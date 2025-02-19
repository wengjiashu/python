import { createRouter, createWebHistory } from 'vue-router';
import ImageEdit from   '../components/ImageEdit.vue';
import CreateImage from '../components/CreateImage.vue';
const routes = [
  {
    path: '/',
    component: CreateImage
  },
  {
    path: '/edit',
    name: 'ImageEdit',
    component: ImageEdit
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;