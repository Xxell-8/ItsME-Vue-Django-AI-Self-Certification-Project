<template>
  <div class="f-column" :key="componentKey">
    <!-- header -->
    <div class="camera-before-header" v-if="isCameraOn">
      <p class="t-white fw-700">얼굴을 테두리 안에 맞추고</p>
      <p class="t-white fw-700"><strong class="text-secondary">촬영</strong> 버튼을 눌러주세요.</p>
    </div>
    <div class="camera-after-header" v-if="isPhotoTaken">
      <p class="t-white fw-700">본인의 얼굴에 테두리가 그려졌다면</p>
      <p class="t-white fw-700"><strong class="text-secondary">다음</strong> 버튼을, 재촬영을 원하시면</p>
      <p class="t-white fw-700"><strong class="text-secondary">재촬영</strong> 버튼을 눌러주세요.</p>
    </div>
    <!-- camera -->
    <div class="f-column camera-container">
      <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay playsinline></video>
    </div>
    <!-- canvas -->
    <canvas class="canvas-jpeg" ref="canvas"></canvas>
    <canvas class="canvas-hidden" ref="hiddenCanvas"></canvas>
    <!-- overlay -->
    <div class="overlay"></div>
    <!-- buttons -->
    <div class="btn-container">
      <button v-if="isCameraOn" class="btn-shot" @click="takePhoto">촬영</button>
      <button v-if="isPhotoTaken" class="btn-shot" @click="restart">재촬영</button>
      <button v-if="isPhotoTaken" class="btn-shot" @click="nextStep">다음</button>
    </div>
    <!-- 코너 테두리 사각형 -->
    <div class="corner">
      <div class="top-left"></div>
      <div class="top-right"></div>
      <div class="bottom-left"></div>
      <div class="bottom-right"></div>
    </div>
  </div>
</template>

<script>
import '@tensorflow/tfjs-core';
import '@tensorflow/tfjs-backend-webgl';
import * as blazeface from '@tensorflow-models/blazeface';
import { mapMutations } from 'vuex';

export default {
  name: 'FaceRecognitionCamera',
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
    ...mapMutations('customer', ['SAVE_PRESENT_FACE']),
    createCameraElement() {
      const constraints = (window.constraints = {
				audio: false,
				video: { height: window.innerHeight, facingMode: { exact: 'user'} },
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
      
      this.isPhotoTaken = !this.isPhotoTaken;

      // 뷰포트 사이즈와 카메라의 시작 위치 구하기
      const vw = window.innerWidth
      const vh = window.innerHeight
      const videoRatio = this.$refs.camera.videoWidth / this.$refs.camera.offsetWidth
      const startX = (this.$refs.camera.videoWidth - vw*videoRatio) / 2
      
      // 현재 카메라 화면을 캔버스에 옮겨 그리기
      const ctx = this.$refs.canvas.getContext('2d');
      ctx.canvas.width = vw
      ctx.canvas.height = vh
      ctx.drawImage(this.$refs.camera, startX, 0, vw*videoRatio, this.$refs.camera.videoHeight, 0, 0, vw, vh);

      // 얼굴 인식
      const prediction = await this.model.estimateFaces(this.$refs.canvas, false)

      // 인식된 고객의 얼굴 부분만 이미지로 저장하기
      const hiddenCtx = this.$refs.hiddenCanvas.getContext('2d');
      prediction.forEach((pred) => {
        const width = pred.bottomRight[0] - pred.topLeft[0]
        const height = pred.bottomRight[1] - pred.topLeft[1]

        this.$refs.hiddenCanvas.width = width*2
        this.$refs.hiddenCanvas.height = height
        hiddenCtx.width = width*2
        hiddenCtx.height = height

        hiddenCtx.drawImage(
          this.$refs.canvas, 
          pred.topLeft[0] - 0.5*width, pred.topLeft[1], width*2, height, 0, 0, width*2, height
          )
      });
      const jpegImg = this.$refs.hiddenCanvas.toDataURL("image/jpeg")
      this.SAVE_PRESENT_FACE(jpegImg)

      // 고객의 얼굴에 테두리 그리기
      prediction.forEach((pred) => {
        ctx.beginPath();
        ctx.lineWidth = "4";
        ctx.strokeStyle = "#BDFF00";
        ctx.rect(
          pred.topLeft[0] - 0.5*(pred.bottomRight[0] - pred.topLeft[0]),
          pred.topLeft[1],
          (pred.bottomRight[0] - pred.topLeft[0])*2,
          pred.bottomRight[1] - pred.topLeft[1]
        );
        ctx.stroke();        
      });

      // 카메라 종료하기
      this.stopCameraStream();
    },
    async initDetector() {
      // Vue3 문제 해결: Object.freeze
      this.model = Object.freeze(await blazeface.load());
    },
    restart() {
      this.componentKey += 1
      this.isCameraOn = false;
      this.isPhotoTaken = false;
      this.isShotPhoto = false;
      this.createCameraElement();
    },
    nextStep() {
      this.$router.push('/customer/motion-recognition')
    }
  }  
}
</script>