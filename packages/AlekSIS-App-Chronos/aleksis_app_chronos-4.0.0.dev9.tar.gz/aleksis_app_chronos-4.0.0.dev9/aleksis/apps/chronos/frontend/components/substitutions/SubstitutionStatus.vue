<template>
  <v-tooltip bottom>
    <template #activator="{ on, attrs }">
      <v-icon
        :color="currentStatus?.color"
        class="mr-md-4"
        v-on="on"
        v-bind="attrs"
        >{{ currentStatus?.icon }}</v-icon
      >
    </template>
    <span>{{ currentStatus?.text }}</span>
  </v-tooltip>
</template>

<script>
export default {
  name: "SubstitutionStatus",
  data() {
    return {
      statusChoices: [
        {
          name: "unedited",
          text: this.$t("chronos.substitutions.overview.status.unedited"),
          icon: "mdi-calendar-question-outline",
          color: "warning",
        },
        {
          name: "substituted",
          text: this.$t("chronos.substitutions.overview.status.substituted"),
          icon: "mdi-calendar-edit-outline",
          color: "success",
        },
        {
          name: "cancelled",
          text: this.$t("chronos.substitutions.overview.status.cancelled"),
          icon: "mdi-cancel",
          color: "error",
        },
      ],
      statusTimeout: null,
      currentStatusName: "",
    };
  },
  props: {
    substitution: {
      type: Object,
      required: true,
    },
  },
  computed: {
    currentStatus() {
      return this.statusChoices.find((s) => s.name === this.currentStatusName);
    },
  },
  methods: {
    updateStatus() {
      if (this.substitution.id.startsWith("DUMMY")) {
        this.currentStatusName = "unedited";
      } else if (this.substitution.cancelled) {
        this.currentStatusName = "cancelled";
      } else {
        this.currentStatusName = "substituted";
      }
    },
  },
  watch: {
    substitution: {
      handler() {
        this.updateStatus();
      },
      deep: true,
    },
  },
  mounted() {
    this.updateStatus();
  },
};
</script>
