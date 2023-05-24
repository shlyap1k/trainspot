<template>
  <div>
    <video ref="videoRef" autoplay></video>
  </div>
</template>

<script>
export default {
  mounted() {
    // Получение доступа к веб-камере и отображение видео
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        this.$refs.videoRef.srcObject = stream;
      })
      .catch(error => {
        console.error('Ошибка при получении доступа к веб-камере:', error);
      });
  }
};
</script>

<style scoped>
video {
  width: 100%;
  max-width: 400px;
}
</style>
