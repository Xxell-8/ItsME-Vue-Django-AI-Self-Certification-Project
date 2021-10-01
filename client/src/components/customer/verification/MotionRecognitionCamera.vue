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
        <div class="motion-box"></div>
        <div class="motion-dialog">
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
      detector: null,
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
      
      // 카메라의 현재 프레임을 canvas에 그리기
      const ctx = this.$refs.canvas.getContext('2d');
      ctx.canvas.width = 320
      ctx.canvas.height = 240
      ctx.drawImage(this.$refs.camera, 0, 0, 320, 240);
      // 고객이 촬영한 이미지를 jpegImg로 저장
      /* const jpegImg = this.$refs.canvas.toDataURL("image/jpeg")
      console.log(jpegImg) */

      // 자세인식 data 쓰지 않고 함수 내의 const로 처리
      const detectorConfig = {
        inputResolution: { width: 320, height: 240 },
        scale: 0.8
      };
      const detector = await posenet.load(detectorConfig)
      const pose = await detector.estimateSinglePose(this.$refs.canvas)
      console.log(pose)

      // skeleton 그리기
      drawKeypoints(pose["keypoints"], 0.55, ctx);
      drawSkeleton(pose["keypoints"], 0.65, ctx);


      // 카메라 종료하기
      this.stopCameraStream();
    },
  }  
}
</script>