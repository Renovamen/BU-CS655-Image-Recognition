<template>
  <div class="container">
    <h1>CS 655: Image Recognition Application</h1>

    <a-form-item>
      <a-form-item name="dragger" no-style>
        <a-upload-dragger name="files" accept="image/*" :customRequest="upload">
          <p class="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p class="ant-upload-text">Click or drag images to this area to upload</p>
        </a-upload-dragger>
      </a-form-item>
    </a-form-item>

    <a-row :gutter="[20, 20]">
      <a-col
        v-for="item in resultList"
        :key="item.requestId"
        :span="12"
      >
        <a-card hoverable style="width: 300px">
          <template #cover>
            <a-image :width="300" :src="HOSTNAME + item.imageUrl" />
          </template>
          <a-card-meta :title="`${item.name} is:`">
            <template #description>
              <div v-if="item.result === undefined">Recognizing...</div>
              <div v-else>{{ item.result || "" }}</div>
            </template>
          </a-card-meta>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue";
import { InboxOutlined } from "@ant-design/icons-vue";
import axios from "axios";
import { io } from "socket.io-client";

const HOSTNAME = "http://127.0.0.1:80";
const API = HOSTNAME + "/api/task";

const resultList = ref<any>([]);
const resultDict = ref<any>({});

// setup socket connection
const socket = io(HOSTNAME);

// get a recognition result from backend and display it
socket.on("result", (data): void => {
  if (data.task_id in resultDict.value) {
    resultDict.value[data.task_id].result = data.result;
  }
})

// disconnect socket
onBeforeUnmount(() => {
  socket.disconnect();
})

// upload an image and send the image to backend
const upload = async ({ onSuccess, onError, file }: any) => {
  const reqData = new FormData();
  reqData.append("file", file);

  try {
    const result = await axios.post(API, reqData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    })

    // backend will return a requestId
    // the image URL will be "upload/{requestId}"
    const requestId = result.data;
    const element = {
      imageUrl: `/upload/${requestId}`,
      requestId: requestId,
      name: file.name,
      result: undefined,
    };

    resultList.value.push(element);
    resultDict.value[requestId] = element;

    onSuccess(file);
  } catch (e: any) {
    console.log("Error: ", e.message);
    onError(null, file);
  }
};
</script>

<style scoped>
.container {
  width: 620px;
  margin: 0 auto;
  padding: 30px 0;
}
</style>
