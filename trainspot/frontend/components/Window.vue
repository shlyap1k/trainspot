<template>
  <div class="window" v-draggable>
    <div class="title-bar" @mousedown="startDrag">
      <slot name="title">Window</slot>
    </div>
    <div class="content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  components: {
    draggable
  },
  directives: {
    draggable: draggable.directive
  },
  data() {
    return {
      dragging: false,
      startX: null,
      startY: null,
      initialX: null,
      initialY: null
    }
  },
  methods: {
    startDrag(event) {
      this.dragging = true
      this.startX = event.clientX
      this.startY = event.clientY
      this.initialX = this.$el.offsetLeft
      this.initialY = this.$el.offsetTop
      document.addEventListener('mousemove', this.doDrag)
      document.addEventListener('mouseup', this.stopDrag)
    },
    doDrag(event) {
      if (this.dragging) {
        const dx = event.clientX - this.startX
        const dy = event.clientY - this.startY
        this.$el.style.left = `${this.initialX + dx}px`
        this.$el.style.top = `${this.initialY + dy}px`
      }
    },
    stopDrag() {
      this.dragging = false
      document.removeEventListener('mousemove', this.doDrag)
      document.removeEventListener('mouseup', this.stopDrag)
    }
  }
}
</script>

<style scoped>
.window {
  position: absolute;
  top: 100px;
  left: 100px;
  width: 400px;
  height: 300px;
  background-color: white;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  z-index: 100;
}

.title-bar {
  height: 30px;
  background-color: #0078d4;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px;
  cursor: move;
}

.content {
  height: calc(100% - 30px);
  padding: 10px;
  overflow: auto;
}
</style>
