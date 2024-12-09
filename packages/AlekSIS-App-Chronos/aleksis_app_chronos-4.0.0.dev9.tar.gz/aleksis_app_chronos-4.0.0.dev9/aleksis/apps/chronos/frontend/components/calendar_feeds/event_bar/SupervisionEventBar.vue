<template>
  <lesson-event-bar :with-subject="false" v-bind="$attrs" v-on="$listeners">
    <template #additionalElements>
      <v-icon size="12" color="white" class="mr-1">mdi-coffee</v-icon>
    </template>
  </lesson-event-bar>
</template>

<script>
import LessonEventBar from "./LessonEventBar.vue";

export default {
  name: "SupervisionEventBar",
  components: {
    LessonEventBar,
  },
  extends: [LessonEventBar],
};
</script>
