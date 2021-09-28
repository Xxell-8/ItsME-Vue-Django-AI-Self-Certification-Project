<template>
  <div class="f-column">
    <!-- header -->
    <div class="camera-header">
      <span class="t-white fw-700 header-text">Face 인식</span>
    </div>
    <!-- camera -->
    <!-- <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay></video> -->
    <div class="f-column">
      <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay></video>
      <div class="face-direction" v-if="isCameraOn">
        <div class="face-box"></div>
        <div class="face-dialog">
          <p>표시된 위치에</p>
          <p>얼굴 정면을 비추고</p>
          <p>촬영 버튼을 눌러주세요!</p>
        </div>
      </div>
    </div>
    <!-- canvas -->
    <canvas class="canvas-jpeg" ref="canvas"></canvas>
    <!-- buttons -->
    <button v-if="isCameraOn" class="btn-shot" @click="takePhoto">촬영</button>
    <button v-if="isPhotoTaken" class="btn-shot">재촬영</button>
    <button v-if="isPhotoTaken" class="btn-shot">다음</button>
  </div>
</template>

<script>
import '@tensorflow/tfjs-backend-cpu'
import '@tensorflow/tfjs-backend-webgl'
import * as cocoSsd from '@tensorflow-models/coco-ssd'

export default {
  name: 'CardRecognitionCamera',
  components: {
  },
  props: {},
  data() {
    return {
      model: null,
      photoTaken: false,
      isCameraOn: false,
      isPhotoTaken: false,
      isShotPhoto: false,
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
      
      this.isPhotoTaken = !this.isPhotoTaken;
      
      const ctx = this.$refs.canvas.getContext('2d');
      ctx.canvas.width = 320
      ctx.canvas.height = 240
      ctx.drawImage(this.$refs.camera, 0, 0, 320, 240);
      
      // 고객이 촬영한 이미지를 jpegImg로 저장
      /* const jpegImg = this.$refs.canvas.toDataURL("image/jpeg")
      console.log(jpegImg) */

      // 객체 인식
      const prediction = await this.model.detect(this.$refs.canvas)
      console.log('Prediction: ')
      console.log(prediction)

      // 카메라 종료하기
      this.stopCameraStream();
    },
    async initDetector() {
      // Vue3 문제 해결: Object.freeze
      this.model = Object.freeze(await cocoSsd.load());
    },
  }  
}
</script>