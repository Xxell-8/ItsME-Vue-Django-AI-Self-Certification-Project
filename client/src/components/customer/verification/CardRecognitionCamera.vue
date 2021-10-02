<template>
  <div class="f-column">
    <!-- header -->
    <div class="camera-header">
      <span class="t-white fw-700 header-text">신분증 촬영</span>
    </div>
    <!-- camera -->
    <!-- <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay></video> -->
    <div class="f-column">
      <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay></video>
      <div class="card-direction" v-if="isCameraOn">
        <div class="card-box"></div>
        <div class="card-dialog">
          <p>표시된 위치에</p>
          <p>신분증을 알맞게 조정하여</p>
          <p>촬영 버튼을 눌러주세요!</p>
        </div>
      </div>
    </div>
    <!-- canvas -->
    <canvas class="canvas-jpeg" ref="canvas"></canvas>
    <canvas class="canvas-hidden" ref="hiddenCanvas"></canvas>
    <!-- buttons -->
    <button v-if="isCameraOn" class="btn-shot" @click="takePhoto">촬영</button>
    <button v-if="isPhotoTaken" class="btn-shot">재촬영</button>
    <button v-if="isPhotoTaken" class="btn-shot">다음</button>
  </div>
</template>

<script>
import '@tensorflow/tfjs-backend-cpu'
import '@tensorflow/tfjs-backend-webgl'
import * as blazeface from '@tensorflow-models/blazeface';

export default {
  name: 'CardRecognitionCamera',
  components: {
  },
  props: {},
  data() {
    return {
      model: null,
      isCameraOn: false,
      isPhotoTaken: false,
      isShotPhoto: false,
      componentKey: 0,
    }
  },
  mounted() {
    this.createCameraElement();
  },
  methods: {
    createCameraElement() {
      const constraints = (window.constraints = {
				audio: false,
				video: { width: 320, height: 240}
			})
      navigator.mediaDevices
				.getUserMedia(constraints)
				.then(stream => {
					this.$refs.camera.srcObject = stream;
          this.isCameraOn = true;
				})
				.catch(error => {
          console.log(error)
					alert("지원하지 않는 브라우저입니다.");
				});
    },
    stopCameraStream() {
      const tracks = this.$refs.camera.srcObject.getTracks()
      tracks.forEach(track => {
        track.stop()
        this.isCameraOn = false;
      })
    },
    async takePhoto() {
      if(!this.isPhotoTaken) {
        this.isShotPhoto = true;

        const TIMEOUT = 50;

        setTimeout(() => {
          this.isShotPhoto = false;
        }, TIMEOUT);
      }
      
      // 신분증 범위만 그려서 저장하기 - 캔버스 사이즈 추후 조정
      const ctx = this.$refs.canvas.getContext('2d');
      ctx.canvas.width = 320
      ctx.canvas.height = 240
      ctx.drawImage(this.$refs.camera, 0, 0, 320, 240);
      const jpegImg = this.$refs.canvas.toDataURL("image/jpeg")
      console.log(jpegImg)

      // 얼굴 인식
      const prediction = await this.model.estimateFaces(this.$refs.canvas, false)

      // 인식된 고객의 얼굴 부분만 이미지로 저장하기
      const hiddenCtx = this.$refs.hiddenCanvas.getContext('2d');
      prediction.forEach((pred) => {
        const width = pred.bottomRight[0] - pred.topLeft[0]
        const height = pred.bottomRight[1] - pred.topLeft[1]

        this.$refs.hiddenCanvas.width = width
        this.$refs.hiddenCanvas.height = height
        hiddenCtx.width = width
        hiddenCtx.height = height

        hiddenCtx.drawImage(
          this.$refs.canvas, 
          pred.topLeft[0], pred.topLeft[1], width, height, 0, 0, width, height
          )
      });
      const faceImg = this.$refs.hiddenCanvas.toDataURL("image/jpeg")
      console.log(faceImg)

      // 카메라 종료하기
      this.stopCameraStream();
    },
    async initDetector() {
      // Vue3 문제 해결: Object.freeze
      this.model = Object.freeze(await blazeface.load());
    },
  }  
}
</script>