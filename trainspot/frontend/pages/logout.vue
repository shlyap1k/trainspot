<template>
  <div></div>
</template>

<script>
export default {
  async created() {
    const data = new FormData();
    data.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"));
    await this.$auth.logout({data: data})
    this.$store.dispatch("user/logoutUser")
  }
}
</script>
