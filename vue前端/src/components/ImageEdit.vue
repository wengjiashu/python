<template>
  <div class="container">
    <h1 style="text-align: center;">发挥想象力，创作属于自己的画布</h1>
    <!-- 工具图标容器 -->
    <div class="tool-icons">
      <h3>绘图工具</h3>
      <el-icon
        @click="toggleTool('brush')"
        :class="{ 'active-icon': currentTool === 'brush' }"
        style="cursor: pointer; font-size: 36px;">
        <Edit />
      </el-icon>
      <el-icon
        @click="toggleTool('eraser')"
        :class="{ 'active-icon': currentTool === 'eraser' }"
        style="cursor: pointer; font-size: 36px;">
        <Close />
      </el-icon>
      <el-icon
        @click="toggleTool('colorBrush')"
        :class="{ 'active-icon': currentTool === 'colorBrush' }"
        style="cursor: pointer; font-size: 36px;">
        <Brush />
      </el-icon>
    </div>
    <div class="canvas-container">
      <canvas ref="backgroundCanvas"></canvas>
      <canvas ref="drawingCanvas"></canvas>
    </div>
    <!-- 将按钮组移到画布容器下方 -->
    <div class="button-group">
      <button @click="showSaveModal" class="save-button">保存</button>
      <button @click="cancelEdit" class="cancel-button">不保存</button>
    </div>

    <!-- 自定义模态框 -->
    <div v-if="isSaveModalVisible" class="modal">
      <div class="modal-content">
        <span class="close" @click="hideSaveModal">&times;</span>
        <h2>保存图片</h2>
        <input v-model="imageName" placeholder="请输入图片名称" />
        <div class="modal-buttons">
          <button @click="hideSaveModal" class="modal-cancel-button">取消</button>
          <button @click="saveImageAndClose" class="modal-confirm-button">确认</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
// 引入 ElementPlus 的图标
import { Edit, Close, Brush } from '@element-plus/icons-vue';

const router = useRouter();
const route = useRoute();
const backgroundCanvas = ref(null);
const drawingCanvas = ref(null);
const backgroundCtx = ref(null);
const drawingCtx = ref(null);
const isDrawing = ref(false);
const lastX = ref(0);
const lastY = ref(0);
const imageName = ref('');
const isSaveModalVisible = ref(false);
// 当前使用的工具，初始为画笔
const currentTool = ref('brush');

const startDrawing = (e) => {
  if (!drawingCtx.value) return;
  isDrawing.value = true;
  const rect = drawingCanvas.value.getBoundingClientRect();
  lastX.value = ((e.clientX - rect.left) / (rect.right - rect.left)) * drawingCanvas.value.width;
  lastY.value = ((e.clientY - rect.top) / (rect.bottom - rect.top)) * drawingCanvas.value.height;
};

const draw = (e) => {
  if (!drawingCtx.value ||!isDrawing.value) return;
  const rect = drawingCanvas.value.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / (rect.right - rect.left)) * drawingCanvas.value.width;
  const y = ((e.clientY - rect.top) / (rect.bottom - rect.top)) * drawingCanvas.value.height;

  drawingCtx.value.beginPath();
  drawingCtx.value.moveTo(lastX.value, lastY.value);
  drawingCtx.value.lineTo(x, y);

  if (currentTool.value === 'brush') {
    drawingCtx.value.strokeStyle = 'black';
    drawingCtx.value.lineWidth = 2;
  } else if (currentTool.value === 'eraser') {
    drawingCtx.value.globalCompositeOperation = 'destination-out';
    drawingCtx.value.lineWidth = 10;
  } else if (currentTool.value === 'colorBrush') {
    drawingCtx.value.strokeStyle = 'red'; // 可根据需求修改颜色
    drawingCtx.value.lineWidth = 2;
  }

  drawingCtx.value.stroke();
  drawingCtx.value.globalCompositeOperation = 'source-over'; // 恢复默认绘制模式
  lastX.value = x;
  lastY.value = y;
};

const stopDrawing = () => {
  isDrawing.value = false;
};

const showSaveModal = () => {
  isSaveModalVisible.value = true;
};

const saveImageAndClose = async () => {
  if (!imageName.value) {
    alert('请输入图片名称');
    return;
  }
  try {
    // 创建一个临时画布，将背景画布和绘制画布合并
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    tempCanvas.width = backgroundCanvas.value.width;
    tempCanvas.height = backgroundCanvas.value.height;
    tempCtx.drawImage(backgroundCanvas.value, 0, 0);
    tempCtx.drawImage(drawingCanvas.value, 0, 0);

    const dataURL = tempCanvas.toDataURL('image/png');
    const response = await fetch('http://127.0.0.1:5000/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        imageData: dataURL,
        imageName: imageName.value
      })
    });

    if (response.ok) {
      alert('图片保存成功！');
      isSaveModalVisible.value = false;
      router.push('/');
    } else {
      alert('图片保存失败，请稍后重试。');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('发生错误，请稍后重试。');
  }
};

const hideSaveModal = () => {
  isSaveModalVisible.value = false;
  imageName.value = '';
};

const cancelEdit = () => {
  router.push('/');
};

const toggleTool = (tool) => {
  currentTool.value = tool;
};

onMounted(() => {
  backgroundCanvas.value = backgroundCanvas.value || document.createElement('canvas');
  drawingCanvas.value = drawingCanvas.value || document.createElement('canvas');
  backgroundCtx.value = backgroundCanvas.value.getContext('2d');
  drawingCtx.value = drawingCanvas.value.getContext('2d');

  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.src = route.query.imageUrl;
  img.onload = () => {
    // 设置画布的实际像素大小
    backgroundCanvas.value.width = img.width;
    backgroundCanvas.value.height = img.height;
    drawingCanvas.value.width = img.width;
    drawingCanvas.value.height = img.height;

    // 设置画布的 CSS 样式大小
    backgroundCanvas.value.style.width = '60%';
    drawingCanvas.value.style.width = '60%';
    backgroundCanvas.value.style.height = 'auto';
    drawingCanvas.value.style.height = 'auto';

    backgroundCtx.value.drawImage(img, 0, 0);
  };

  drawingCanvas.value.addEventListener('mousedown', startDrawing);
  drawingCanvas.value.addEventListener('mousemove', draw);
  drawingCanvas.value.addEventListener('mouseup', stopDrawing);
  drawingCanvas.value.addEventListener('mouseout', stopDrawing);
});
</script>

<style scoped>
.container {
  padding: 20px;
  height: 1000px;
  background-color: azure;
}

.canvas-container {
  position: relative;
  margin-top: 20px;
  /* 为画布容器设置底部外边距，让按钮和画布有间隔 */
  margin-bottom: 20px;
}

canvas {
  border: 1px solid black;
  position: absolute;
  top: 15px;
  left: 20%;
}

.tool-icons {
  border: 1px solid black;
  position: absolute;
  right: 5%;
  top: 10%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.tool-icons h3 {
  margin-bottom: 10px;
}

.tool-icons el-icon {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  padding: 10px;
  margin-bottom: 15px;
}

.active-icon {
  color: blue;
  transform: scale(1.2);
  background-color: rgba(0, 123, 255, 0.3);
}

.button-group {
  /* 将按钮组水平居中 */
  display: flex;
  justify-content: center;
  position: relative;
  top: 750px;
}

.save-button,
.cancel-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  /* 增大按钮的内边距以放大按钮 */
  padding: 15px 30px;
  cursor: pointer;
  margin: 0 10px;
  transition: background-color 0.3s ease;
  /* 增大字体大小 */
  font-size: 18px;
}

.save-button:hover,
.cancel-button:hover {
  background-color: #0056b3;
}

.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 30%;
  position: relative;
  border-radius: 10px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.modal-cancel-button,
.modal-confirm-button {
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  margin-left: 10px;
  transition: background-color 0.3s ease;
}

.modal-cancel-button:hover {
  background-color: #5a6268;
}

.modal-confirm-button {
  background-color: #28a745;
}

.modal-confirm-button:hover {
  background-color: #218838;
}
</style>