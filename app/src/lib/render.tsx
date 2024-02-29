import { defineComponent } from 'vue'

export default defineComponent({
  name: 'RenderFunction',
  props: {
    render: {
      required: true,
    },
  },
  render() {
    return this.render
  },
})
