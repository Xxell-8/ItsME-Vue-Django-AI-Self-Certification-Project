<template>
  <div class="home">
    <div class="logo">
      <div class="f-row">
        <img src="@/assets/image/logo/dark-sm.svg" alt="">
        <div class="title font-mont">It's Me!</div>
      </div>
      <button
        class="btn-primary font-mont fw-500"
        @click="$router.push({ name: 'PartnerHome'})"
      >Partners</button>
    </div>
    <div class="intro">
      <div class="f-column-start text">
        <div class="title">본인 인증 통합 솔루션, <span>잇츠미</span></div>
        <div class="descript">
          잇츠미는 인공지능 기술을 활용해 보다 정확하고 간편한 본인 인증 절차를 만들어갑니다. <br/>
          고객의 얼굴과 신분증 사진을 대조하고,
          실시간 모션 인식을 통해 본인 확인을 진행합니다.
          뿐만 아니라 신분증 OCR을 통해 빠르고 편리한 정보 확인은 물론,
          비식별화 기술로 개인 정보를 안전하게 처리할 수 있습니다.<br/>
          이 모든 과정을 웹 URL 하나로 해결하며, 
          워크 플랫폼을 통해 간편하게 본인 인증 결과를 확인할 수 있습니다.<br/>
        </div>
        
      </div>
      <img src="@/assets/image/home/faceDetect.jpg" alt="">
    </div>
    <div class="tech">
      <div class="point font-mont">
        All you need is ONLY
        <span>It's ME!</span>
      </div>
      <div class="body">
        <div class="content">
          <img src="@/assets/image/home/faceDetection.svg" alt="">
          <span class="title">얼굴 인식</span>
          <span class="descript">AI가 사용자의 얼굴 영역을 인식하여, 촬영된 얼굴과 신분증 사진 대조하여 본인 여부를 판단합니다.</span>
        </div>
        <div class="content">
          <img src="@/assets/image/home/recognition.svg" alt="">
          <span class="title">모션 인식</span>
          <span class="descript">사용자에게 랜덤 모션을 제시하고 실시간 영상으로 모션 인식을 진행합니다.</span>
        </div>
        <div class="content">
          <img src="@/assets/image/home/guarantee.svg" alt="">
          <span class="title">안전한 정보 처리</span>
          <span class="descript">본인 인증을 위해 사용한 이미지와 정보는 인증 완료 즉시 파기합니다. </span>
        </div>
      </div>
    </div>
    <div class="footer">
      <span>
        Copyright ©2021 All rights reserved.
        It's ME! made by Team A204 in SSAFY 5th.
      </span>
    </div>
    
  </div>
</template>

<script>
import './home.scss'
export default {
  name: 'Home',
}
</script>