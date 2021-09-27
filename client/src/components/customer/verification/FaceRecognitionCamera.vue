<template>
  <div class="f-column">
    <!-- header -->
    <div class="camera-header">
      <span class="t-white fw-700 header-text">Face 인식</span>
    </div>
    <!-- camera -->
    <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay></video>
    <!-- canvas -->
    <canvas class="canvas-face" ref="canvas"></canvas>
    <!-- buttons -->
    <button class="t-white">사진찍기</button>
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
      photoTaken: false,
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
      })
    },
    async detectFaces() 
    {
      const camera = this.$refs.camera
      const canvas = this.$refs.canvas
      const ctx = canvas.getContext("2d")
      const prediction = await this.model.estimateFaces(camera, false)
      
      ctx.canvas.width = 320
      ctx.canvas.height = 240
      ctx.drawImage(camera, 0, 0, 320, 240)
      /* 얼굴 주변 사각형 그리기 */
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
    },
    async initDetector() {
      // Vue3 문제 해결: Object.freeze
      this.model = Object.freeze(await blazeface.load());
      if (!this.photoTaken) {
        setInterval(this.detectFaces, 100)
      }
    }
  }  
}
</script>