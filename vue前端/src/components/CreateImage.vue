<template>
  <body class="a">
    <div class="container">
      <h1 style="text-align: center;">超级AI画布</h1>
      <input v-model="emo" placeholder="输入你的心情" class="input-field">
      <button @click="generateImage" :disabled="isGenerating" class="generatebutton">生成图片</button>
      <p v-if="isGenerating" class="loadingtext">正在生成图片，请稍候...</p>
        <img v-if ="imageUrl" :src="imageUrl" alt="Generated Image" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave" @click="editImage" class="generatedimage" width="70%" height="70%">
        <div class="tooltip" v-if="isHovered">点击进入创作</div>
    </div>
    <br>
    <HistoryImages />
  </body>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import HistoryImages from './HistoryImages.vue';

const emo = ref('我很高兴');
const imageUrl = ref(null);
const isGenerating = ref(false);
const isHovered = ref(false);

const generateImage = async () => {
  isGenerating.value = true;
  try {
    const response = await fetch('http://127.0.0.1:5000/main', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        emo: emo.value
      })
    });

    if (response.ok) {
      const blob = await response.blob();
      imageUrl.value = URL.createObjectURL(blob);
      alert('图片生成成功！');
    } else {
      console.error('Failed to generate image');
      alert('图片生成失败，请稍后重试。');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('发生错误，请稍后重试。');
  } finally {
    isGenerating.value = false;
  }
};

const router = useRouter();
const editImage = () => {
  if (imageUrl.value) {
    router.push({
      name: 'ImageEdit',
      query: {
        imageUrl: imageUrl.value
      }
    });
  }
};

const handleMouseEnter = () => {
  isHovered.value = true;
};

const handleMouseLeave = () => {
  isHovered.value = false;
};
</script>

<style scoped>
.a {
  background-color: #f0f0f5;
  font-family: Arial,sans-serif;
  height: 1500px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  border-radius: 5px;
}

.input-field {
  width: 70%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.generatebutton {
  margin-bottom: 15px;
  width: 15%;
  position: absolute;
  right: 20%;
  font-size: 27px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  padding: 10px;
  border-radius: 5px;
}

.generatebutton:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loadingtext {
  color: #999;
  margin-bottom: 15px;
}

.generatedimage {
  max-width: 100%;
  height: auto;
  border: 1px solid #ccc;
  border-radius: 3px;
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
}

.imagewrapper {
  position: relative;
  display: inline-block;
}

.tooltip {
  position: absolute;
  top: 400px;
  left: 40%;
  background-color: rgba(0,0,0,0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 24px;
  
}


.imagewrapper:hover.tooltip {
  opacity: 1;
}
</style>