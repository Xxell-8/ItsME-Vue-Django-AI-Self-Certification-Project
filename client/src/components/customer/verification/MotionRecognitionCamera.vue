<template>
  <div class="f-column">
    <!-- camera -->
    <div class="f-column camera-container">
      <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay playsinline></video>
    </div>
    <!-- canvas -->
    <canvas class="canvas-jpeg" ref="canvas"></canvas>
    <!-- direction message -->
    <div class="direction fw-700 t-white">
      <span><strong class="t-green">왼손</strong>을 <strong class="t-green">위로</strong> 높이 들어주세요!</span>
    </div>
  </div>
</template>

<script>
import '@tensorflow/tfjs-core';
import '@tensorflow/tfjs-backend-webgl';
import * as posenet from "@tensorflow-models/posenet";
import { drawKeypoints, drawSkeleton } from "./utilities";

export default {
  name: 'MotionRecognitionCamera',
  components: {
  },
  props: {},
  data() {
    return {
      photoTaken: false,
      isCameraOn: false,
      isPhotoTaken: false,
      isShotPhoto: false,
      isCompleted: false,
      interval: null,
    }
  },
  mounted() {
    this.createCameraElement();
  },
  methods: {
    createCameraElement() {
      const constraints = (window.constraints = {
				audio: false,
				video: { height: window.innerHeight, facingMode: { exact: 'user'} }
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
    async detectPose(detector, ctx) {
      
      // 뷰포트 사이즈와 카메라의 시작 위치 구하기
      const vw = window.innerWidth
      const vh = window.innerHeight
      const videoRatio = this.$refs.camera.videoWidth / this.$refs.camera.offsetWidth
      const startX = (this.$refs.camera.videoWidth - vw*videoRatio) / 2
      
      // 현재 카메라 화면을 캔버스에 옮겨 그리기
      ctx.canvas.width = vw
      ctx.canvas.height = vh
      ctx.drawImage(this.$refs.camera, startX, 0, vw*videoRatio, this.$refs.camera.videoHeight, 0, 0, vw, vh);

      const pose = await detector.estimateSinglePose(this.$refs.canvas)
      
      drawKeypoints(pose["keypoints"], 0.55, ctx);
      drawSkeleton(pose["keypoints"], 0.65, ctx);

      // 왼손 들 때 끝내도록
      if (pose["keypoints"][2]["position"]["y"] - pose["keypoints"][9]["position"]["y"] > 70) {
        this.isCompleted = true;
        clearInterval(this.interval)
        this.stopCameraStream();
        this.nextStep();
      }
      
    },
    async initDetector() {
      const detectorConfig = {
        inputResolution: { width: 320, height: 240 },
        scale: 0.8
      };
      const ctx = this.$refs.canvas.getContext('2d');
      ctx.canvas.width = 320
      ctx.canvas.height = 240
      const detector = await posenet.load(detectorConfig)
      this.interval = setInterval(this.detectPose, 100, detector, ctx)
    },
    nextStep() {
      this.$router.push('/customer/card-recognition')
    }
  }  
}
</script>