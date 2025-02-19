<template>
  <div style="position: relative;">
    <!-- 历史图片导航 -->
    <h1 @click="toggleImageNames" class="history-title">历史图片</h1>
    <!-- 二级导航，显示图片名字 -->
    <span class="list">
      <ul v-if="showImageNames" class="imageNamesList">
        <li v-for="image in historyImages" :key="image.id" class="imageNameItem" @click="renderImage(image.id, image.name)">
          {{ image.name }}
          <button @click="deleteImage(image.id)">删除</button>
        </li>
      </ul>
    </span>
    <!-- 显示选中的图片 selectedImageUrl && showImageNames-->
    <img v-if="showImage" :src="selectedImageUrl" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave" @click="editImage" alt="选中的图片" class="selected-image" width="60%" height="60%">
    <div class="tooltip" v-if="isHovered">点击进入创作</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const isHovered = ref(false);
// 存储历史图片信息
const historyImages = ref([]);
// 控制二级导航是否显示
const showImageNames = ref(false);
// 存储选中图片的 URL
const selectedImageUrl = ref('');
// 存储选中图片的名字
const selectedImageName = ref('');
const showImage = ref(false);

// 获取历史图片信息
const fetchHistoryImages = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/history-images');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    historyImages.value = data;
  } catch (error) {
    console.error('Error fetching history images:', error);
  }
};

// 切换二级导航的显示状态
const toggleImageNames = () => {
  showImageNames.value =!showImageNames.value;
  if (!showImageNames.value) {
    showImage.value = false;
  }
};

// 渲染选中的图片
const renderImage = (image_id, name) => {
  selectedImageUrl.value = `http://127.0.0.1:5000/image/${image_id}`;
  selectedImageName.value = name;
  showImage.value = true;
};

// 组件挂载时获取历史图片信息
onMounted(() => {
  fetchHistoryImages();
});

const router = useRouter();
const editImage = () => {
  if (selectedImageUrl.value) {
    router.push({
      name: 'ImageEdit',
      query: {
        imageUrl: selectedImageUrl.value
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

// 删除图片方法
const deleteImage = async (imageId) => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/delete-image/${imageId}`, {
      method: 'DELETE'
    });
    if (response.ok) {
      // 删除成功，更新历史图片列表
      await fetchHistoryImages();
    } else {
      console.error('Failed to delete image');
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
</script>

<style scoped>
.history-title {
  cursor: pointer;
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
  text-decoration: underline;
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

.list {
  position: absolute;
  width: 20%;
  height: auto;
}

.imageNamesList {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.imageNameItem {
  cursor: pointer;
  color: #666;
  font-size: 16px;
  padding: 5px 10px;
  transition: background-color 0.2s ease-in-out;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.imageNameItem button {
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 3px;
  padding: 5px 10px;
  cursor: pointer;
}

.imageNameItem button:hover {
  background-color: #c82333;
}

.selected-image {
  margin-top: 20px;
  margin-left: 22%;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(223, 187, 8, 0.236);
}
</style>