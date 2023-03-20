<template>
<div>
  <p>message.text</p>
</div>
</template>

<script>
  export default {
    name: "MessageBlock",
    props: {
      message: {
        type: Object,
        required: true
      },
    },
  }
</script>

