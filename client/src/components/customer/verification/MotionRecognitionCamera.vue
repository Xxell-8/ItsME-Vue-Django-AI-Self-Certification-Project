<template>
  <div class="f-column">
    <!-- header -->
    <div class="camera-header">
      <span class="t-white fw-700 header-text">실시간 모션 인식</span>
    </div>
    <!-- camera -->
    <!-- <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay></video> -->
    <div class="f-column">
      <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay></video>
      <div class="motion-direction" v-if="isCameraOn">
        
      </div>
    </div>
    <!-- canvas -->
    <canvas class="canvas-jpeg" ref="canvas"></canvas>
    <div class="motion-dialog">
      <p>왼손을</p>
      <p>위로 높이</p>
      <p>뻗어주세요!</p>
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
    async detectPose(detector, ctx) {
      
      ctx.drawImage(this.$refs.camera, 0, 0, 320, 240);

      const pose = await detector.estimateSinglePose(this.$refs.canvas)
      
      drawKeypoints(pose["keypoints"], 0.55, ctx);
      drawSkeleton(pose["keypoints"], 0.65, ctx);

      // 왼손 들 때 끝내도록
      if (pose["keypoints"][2]["position"]["y"] - pose["keypoints"][9]["position"]["y"] > 30) {
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