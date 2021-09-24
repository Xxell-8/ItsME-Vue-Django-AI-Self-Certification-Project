<template>
  <div class="f-column">
    <div class="camera-header">
      <span class="t-white fw-700 header-text">FACE 인식</span>
    </div>
    <video class="camera-stream" ref="camera" autoplay></video>
    <canvas class="canvas-face"></canvas>
  </div>
</template>

<script>

export default {
  name: 'FaceRecognitionCamera',
  components: {
  },
  props: {},
  data() {
    return {}
  },
  created() {
    this.createCameraElement()
  },
  methods: {
    createCameraElement() {
      const constraints = (window.constraints = {
				audio: false,
				video: true
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
    }
  }
}
</script>