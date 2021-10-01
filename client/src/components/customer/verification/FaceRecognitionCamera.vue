<template>
  <div class="f-column" :key="componentKey">
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
    <button v-if="isPhotoTaken" class="btn-shot" @click="restart">재촬영</button>
    <button v-if="isPhotoTaken" class="btn-shot" @click="nextStep">다음</button>
  </div>
</template>

<script>
import '@tensorflow/tfjs-core';
import '@tensorflow/tfjs-backend-webgl';
import * as blazeface from '@tensorflow-models/blazeface';

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
      const jpegImg = this.$refs.canvas.toDataURL("image/jpeg")
      console.log(jpegImg)

      // 고객의 얼굴에 테두리 그리기
      const prediction = await this.model.estimateFaces(this.$refs.canvas, false)
      prediction.forEach((pred) => {
        ctx.beginPath();
        ctx.lineWidth = "4";
        ctx.strokeStyle = "blue";
        ctx.rect(
          pred.topLeft[0],
          pred.topLeft[1],
          pred.bottomRight[0] - pred.topLeft[0],
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