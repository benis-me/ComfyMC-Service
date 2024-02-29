'use strict'
import { app } from '../../scripts/app.js'
import { api } from '../../scripts/api.js'

class IframeAPI {
  constructor() {}

  static postMessage(eventType, data) {
    window.parent.postMessage(
      {
        from: 'comfymc',
        type: eventType,
        payload: data,
      },
      '*'
    )
  }

  handleMessage(event) {
    const eventData = event.data

    if (eventData.internal) {
      const internalData = eventData.internal
      this.handleInternalMessage(internalData)
    }
  }

  handleInternalMessage(internalData) {
    switch (internalData.type) {
      case 'load-prompt':
        if (internalData.payload && internalData.payload.prompt) {
          this.loadPrompt(internalData.payload.prompt)
        }
        break
      case 'get-prompt':
        app
          .graphToPrompt()
          .then((prompt) => {
            const nodes = []
            for (const nodeData of prompt.workflow.nodes) {
              const node = this.app.graph.getNodeById(nodeData.id)
              const { id, title, type, inputs, outputs, widgets } = node
              if (node) {
                nodes.push({
                  id,
                  title,
                  type,
                  inputs: inputs
                    ? inputs.map((input) =>
                        this.pickProperties(input, ['name', 'type', 'link'])
                      )
                    : [],
                  outputs: outputs
                    ? outputs.map((output) => ({
                        ...this.pickProperties(output, [
                          'name',
                          'type',
                          'links',
                          'slot_index',
                        ]),
                        title: output.name,
                      }))
                    : [],
                  widgets: widgets
                    ? widgets.map((widget) => ({
                        ...this.pickProperties(widget, [
                          'name',
                          'type',
                          'value',
                          'options',
                        ]),
                        title: widget.name,
                      }))
                    : [],
                })
              }
            }

            prompt.nodes = nodes
            IframeAPI.postMessage(
              'got-prompt',
              JSON.parse(JSON.stringify(prompt))
            )
            this.updateGraph(prompt)
          })
          .catch((e) => {
            console.error(e)
            IframeAPI.postMessage('prompt-gen-error')
          })
        break
      case 'refresh-defs':
        this.app.refreshComboInNodes()
        break
      case 'export':
        app
          .graphToPrompt()
          .then((prompt) =>
            IframeAPI.postMessage('download-prompt', prompt.workflow)
          )
          .catch((error) =>
            IframeAPI.postMessage('prompt-gen-error', error?.message)
          )
        break
      case 'import':
        const fileInput = document.getElementById('comfy-file-input')
        if (fileInput) fileInput.click()
        break
      case 'clear':
        this.app.clean()
        this.app.graph.clear()
        break
      case 'undo':
        this.triggerKeyboardEvent('z', true)
        break
      case 'redo':
        this.triggerKeyboardEvent('y', true)
        break
      case 'zoom-in':
        this.app.canvas.setZoom(this.app.canvas.ds.scale + 0.2)
        break
      case 'zoom-out':
        this.app.canvas.setZoom(this.app.canvas.ds.scale - 0.2)
        break
      case 'zoom-reset':
        this.resetZoom()
        break
      case 'editor-settings':
        this.app.ui.settings.show()
        break
      case 'arrange':
        this.app.graph.arrange()
        break
      case 'open-manager':
        const managerButton = document.querySelector('.manager-button')
        if (managerButton) managerButton.click()
        break
      case 'queue-prompt':
        this.app.queuePrompt(0)
        break
    }
  }

  pickProperties(obj, properties) {
    return properties.reduce((acc, property) => {
      if (obj[property]) {
        acc[property] = obj[property]
      }
      return acc
    }, {})
  }

  triggerKeyboardEvent(key, ctrlKey) {
    const event = new KeyboardEvent('keydown', { key: key, ctrlKey: ctrlKey })
    window.dispatchEvent(event)
  }

  resetZoom() {
    const bounds = this.app.graph._nodes.reduce(
      (acc, node) => {
        acc[0] = Math.min(acc[0], node.pos[0])
        acc[1] = Math.min(acc[1], node.pos[1])
        const nodeBounds = node.getBounding()
        acc[2] = Math.max(acc[2], node.pos[0] + nodeBounds[2])
        acc[3] = Math.max(acc[3], node.pos[1] + nodeBounds[3])
        return acc
      },
      [99999, 99999, -99999, -99999]
    )

    const margin = 50
    bounds[0] -= margin
    bounds[1] -= margin
    bounds[2] += margin
    bounds[3] += margin

    const offsetX = -bounds[0]
    const offsetY = -bounds[1]
    this.app.canvas.setZoom(1)
    this.app.canvas.ds.offset = new Float32Array([offsetX, offsetY])
    this.app.canvas.draw(true, true)
  }

  loadPrompt(promptData) {
    const setupPrompt = () => {
      if (promptData.viewport) {
        const { x, y, scale } = promptData.viewport
        this.app.canvas.setZoom(scale)
        this.app.canvas.ds.offset = new Float32Array([x, y])
        this.app.canvas.draw(true, true)
      }

      if (promptData.read_only) {
        this.readOnly = true
        this.disableUserInteraction()
      } else {
        setInterval(() => this.saveGraphData(), 500)
      }
    }

    const funcType = this.app.loadGraphData.constructor.name

    if (funcType === 'AsyncFunction') {
      this.app
        .loadGraphData(promptData, true)
        .then(() => {
          setupPrompt()
          IframeAPI.postMessage('prompt-loaded')
        })
        .catch(() => {
          setupPrompt()
          IframeAPI.postMessage('prompt-load-error')
        })
    } else {
      this.app.loadGraphData(promptData, true)
      setupPrompt()
      IframeAPI.postMessage('prompt-loaded')
    }
  }

  disableUserInteraction() {
    const graphProptypes = Object.getPrototypeOf(this.app.graph)
    Object.assign(graphProptypes, {
      getNodeOnPos: () => null,
      processContextMenu: () => null,
    })
    Object.setPrototypeOf(this.app.graph, graphProptypes)

    const canvasProptypes = Object.getPrototypeOf(this.app.canvas)
    Object.assign(canvasProptypes, {
      processContextMenu: () => null,
      showSearchBox: () => null,
      showLinkMenu: () => null,
      processKey: () => null,
    })
    Object.setPrototypeOf(this.app.canvas, canvasProptypes)

    Array.from(document.querySelectorAll('[type="file"]')).forEach((element) =>
      element.remove()
    )
    Array.from(
      document.querySelectorAll(
        '.comfy-modal, .comfy-menu, .comfy-settings-dialog'
      )
    ).forEach((element) => element.remove())
    Array.from(document.querySelectorAll('input, textarea, select')).forEach(
      (element) => (element.style.pointerEvents = 'none')
    )

    const preventDefaultAndStopPropagation = (event) => {
      event.preventDefault()
      event.stopImmediatePropagation()
    }

    document.addEventListener('drop', preventDefaultAndStopPropagation, true)
    document.addEventListener('paste', preventDefaultAndStopPropagation, true)
    document.addEventListener('copy', preventDefaultAndStopPropagation, true)

    this.resetZoom()
  }

  saveGraphData() {
    const [offsetX, offsetY] = this.app.canvas.ds.offset
    const scale = this.app.canvas.ds.scale
    const graphData = this.app.graph.serialize()
    graphData.viewport = { x: offsetX, y: offsetY, scale: scale }
    IframeAPI.postMessage('graph-data', graphData)
  }

  updateGraph(graphData) {
    this.app.lastNodeErrors = null
    this.app.canvas.draw(true, true)

    for (const nodeData of graphData.workflow.nodes) {
      const node = this.app.graph.getNodeById(nodeData.id)
      if (node.widgets) {
        node.widgets.forEach((widget) => {
          if (widget.afterQueued) {
            widget.afterQueued()
          }
        })
      }
    }
  }

  extendAppWithMissingNodesError() {
    const appPrototype = Object.getPrototypeOf(this.app)
    Object.assign(appPrototype, {
      showMissingNodesError: (missingNodes) => {
        if (missingNodes.length > 0) {
          IframeAPI.postMessage(
            'missing-nodes',
            Array.from(
              new Set(missingNodes.filter((node) => typeof node === 'string'))
            )
          )
        }
      },
    })
    Object.setPrototypeOf(this.app, appPrototype)
  }

  initApp() {
    document
      .querySelectorAll('.comfy-menu')
      .forEach((el) => (el.style.display = 'none'))

    this.app.canvas.show_info = false
    this.extendAppWithMissingNodesError()
    window.addEventListener('message', this.handleMessage.bind(this))

    let count = 0
    return new Promise((resolve) => {
      let interval = setInterval(() => {
        count++
        const els = document.querySelectorAll('.comfy-menu')
        const allHidden = Array.from(els).every(
          (el) => el.style.display === 'none'
        )
        if (allHidden) {
          clearInterval(interval)
          resolve()
        }
        if (count > 1000) {
          clearInterval(interval)
          resolve()
        }
      }, 100)
    })
  }

  async init(app) {
    this.app = app
    await this.initApp()
    IframeAPI.postMessage('loaded')
  }
}

const iframeApi = new IframeAPI()

app.registerExtension({
  name: 'ComfyMC.IframeAPI',
  setup() {
    if (self !== top) {
      iframeApi.init(app)
      socketListener()
    }
  },
})

const processMouseDown = LGraphCanvas.prototype.processMouseDown
LGraphCanvas.prototype.processMouseDown = function (e) {
  IframeAPI.postMessage('graphcanvas-mousedown')
  return processMouseDown.apply(this, arguments)
}

const processMouseUp = LGraphCanvas.prototype.processMouseUp
LGraphCanvas.prototype.processMouseUp = function (e) {
  IframeAPI.postMessage('graphcanvas-mouseup')
  return processMouseUp.apply(this, arguments)
}

function socketListener() {
  const types = [
    'status',
    'progress',
    'execution_start',
    'b_preview',
    'executing',
    'executed',
    'execution_cached',
    'execution_error',
  ]

  types.forEach((type) => {
    api.addEventListener(type, ({ detail }) => {
      IframeAPI.postMessage('socket-' + type, detail)
    })
  })
}
