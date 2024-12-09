<script>
export default {
  name: "LessonRelatedObjectChip",
  props: {
    status: {
      type: String,
      default: "regular",
      validator: (value) => ["new", "removed", "regular"].includes(value),
    },
    newIcon: {
      type: String,
      default: "mdi-plus",
    },
  },
};
</script>

<template>
  <v-chip
    label
    outlined
    :class="{
      'mr-2': true,
      'text-decoration-line-through text--secondary': status === 'removed',
    }"
    :color="status === 'new' ? 'warning' : ''"
  >
    <v-icon left v-if="status === 'new'">{{ newIcon }}</v-icon>

    <slot></slot>
  </v-chip>
</template>
