<template>
  <div class="f-column" :key="componentKey">
    <!-- header -->
    <div class="camera-before-header" v-if="isCameraOn">
      <p class="t-white fw-700">주민등록증을 테두리 안에 맞추고</p>
      <p class="t-white fw-700"><strong class="text-secondary">촬영</strong> 버튼을 눌러주세요.</p>
    </div>
    <div class="camera-after-header" v-if="isPhotoTaken">
      <p class="t-white fw-700">테두리 내부의 주민등록증 사진을 확인하고</p>
      <p class="t-white fw-700"><strong class="text-secondary">제출</strong> 버튼을 눌러주세요.</p>
    </div>
    <!-- camera -->
    <div class="f-column camera-container">
      <video @loadeddata="initDetector" class="camera-stream" ref="camera" autoplay playsinline></video>
    </div>
    <!-- canvas -->
    <canvas class="canvas-jpeg" ref="canvas"></canvas>
    <canvas class="canvas-hidden" ref="cardCanvas"></canvas>
    <canvas class="canvas-hidden" ref="hiddenCanvas"></canvas>
    <!-- overlay -->
    <div class="overlay"></div>
    <!-- 코너 테두리 사각형 -->
    <div class="corner">
      <div class="top-left"></div>
      <div class="top-right"></div>
      <div class="bottom-left"></div>
      <div class="bottom-right"></div>
    </div>
    <!-- buttons -->
    <div class="btn-container">
      <button v-if="isCameraOn" class="btn-shot" @click="takePhoto">촬영</button>
      <button v-if="isPhotoTaken" class="btn-shot" @click="restart">재촬영</button>
      <button v-if="isPhotoTaken" class="btn-shot" @click="nextStep">제출</button>
    </div>
  </div>
</template>

<script>
import '@tensorflow/tfjs-backend-cpu'
import '@tensorflow/tfjs-backend-webgl'
import * as blazeface from '@tensorflow-models/blazeface';
import { mapMutations } from 'vuex'

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
    ...mapMutations('customer', ['SAVE_CARD_FACE', 'SAVE_ID_CARD']),
    createCameraElement() {
      const constraints = (window.constraints = {
				audio: false,
				video: { height: window.innerHeight, facingMode: 'environment' }
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

      // 신분증 범위만 그려서 저장하기 - 캔버스 사이즈 추후 조정
      const cardCtx = this.$refs.cardCanvas.getContext('2d');
      const cardWidth = 0.8*vw
      const cardHeight = 0.8*vw*1.6

      this.$refs.cardCanvas.width = cardWidth
      this.$refs.cardCanvas.height = cardHeight
      cardCtx.width = cardWidth
      cardCtx.height = cardHeight

      cardCtx.drawImage(this.$refs.canvas, 0.1*vw, 80, cardWidth, cardHeight, 0, 0, cardWidth, cardHeight);
      
      const jpegImg = this.$refs.cardCanvas.toDataURL("image/jpeg")
      this.SAVE_ID_CARD(jpegImg)
      console.log(jpegImg)

      // 얼굴 인식
      const prediction = await this.model.estimateFaces(this.$refs.cardCanvas, false)

      // 인식된 고객의 얼굴 부분만 이미지로 저장하기
      const hiddenCtx = this.$refs.hiddenCanvas.getContext('2d');
      prediction.forEach((pred) => {
        const width = pred.bottomRight[0] - pred.topLeft[0]
        const height = pred.bottomRight[1] - pred.topLeft[1]

        this.$refs.hiddenCanvas.width = width
        this.$refs.hiddenCanvas.height = height*2
        hiddenCtx.width = width
        hiddenCtx.height = height*2

        hiddenCtx.drawImage(
          this.$refs.cardCanvas, 
          pred.topLeft[0], pred.topLeft[1] - 0.5*height, width, height*2, 0, 0, width, height*2
          )
      });
      const faceImg = this.$refs.hiddenCanvas.toDataURL("image/jpeg")
      this.SAVE_CARD_FACE(faceImg)
      console.log(faceImg)

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
      this.$router.push('/customer/result')
    }
  }  
}
</script>