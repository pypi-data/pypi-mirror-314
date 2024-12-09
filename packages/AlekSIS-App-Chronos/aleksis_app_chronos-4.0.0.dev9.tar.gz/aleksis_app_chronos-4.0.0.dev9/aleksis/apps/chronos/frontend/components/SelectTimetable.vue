<script>
import timetableTypes from "./timetableTypes";
import Mascot from "aleksis.core/components/generic/mascot/Mascot.vue";

export default {
  name: "SelectTimetable",
  components: {
    Mascot,
  },
  props: {
    value: {
      type: Object,
      required: false,
      default: null,
    },
    availableTimetables: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
    limitHeight: {
      default: false,
      required: false,
      type: Boolean,
    },
  },
  data() {
    return {
      selected: null,
      selectedFull: null,
      search: "",
      selectedType: "GROUP",
      types: timetableTypes,
    };
  },
  watch: {
    value(val) {
      this.selectedFull = val;
      this.selected = val.id;
    },
    selectedFull(val) {
      this.$emit("input", val);
    },
  },
  computed: {
    availableTimetablesFiltered() {
      // Filter timetables by selected types
      return this.availableTimetables.filter((timetable) => {
        return this.selectedType == timetable.type;
      });
    },
  },
};
</script>

<template>
  <div>
    <v-card-text class="mb-0">
      <!-- Search field for timetables -->
      <v-text-field
        search
        dense
        filled
        rounded
        clearable
        autofocus
        v-model="search"
        :placeholder="$t('chronos.timetable.search')"
        prepend-inner-icon="mdi-magnify"
        hide-details="auto"
        class="mb-3"
      />

      <!-- Filter by timetable types -->
      <v-btn-toggle v-model="selectedType" dense block class="d-flex" mandatory>
        <v-btn
          v-for="type in types"
          :key="type.id"
          class="flex-grow-1"
          :value="type.id"
        >
          {{ $t(type.name) }}
        </v-btn>
      </v-btn-toggle>
    </v-card-text>

    <!-- Select of available timetables -->
    <v-data-iterator
      :items="availableTimetablesFiltered"
      item-key="id"
      :search="search"
      single-expand
      disable-pagination
      hide-default-footer
      :loading="loading"
      :style="{ height: limitHeight ? '600px' : null }"
      :class="{ 'overflow-auto': limitHeight }"
    >
      <template #default="{ items, isExpanded, expand }">
        <v-list class="scrollable-list">
          <v-list-item-group v-model="selected">
            <v-list-item
              v-for="item in items"
              @click="selectedFull = item"
              :value="item.id"
              :key="item.id"
            >
              <v-list-item-icon color="primary">
                <v-icon v-if="item.type in types" color="secondary">
                  {{ types[item.type].icon }}
                </v-icon>
                <v-icon v-else color="secondary">mdi-grid</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ item.name }}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon>mdi-chevron-right</v-icon>
              </v-list-item-action>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </template>
      <template #loading>
        <v-skeleton-loader type="list-item-avatar@10" />
      </template>
      <template #no-results>
        <div class="d-flex flex-column align-center justify-center">
          <mascot type="searching" width="33%" min-width="250px" />
          <div class="mb-2">
            {{ $t("$vuetify.dataIterator.noResultsText") }}
          </div>
        </div>
      </template>
      <template #no-data>
        <div class="d-flex flex-column align-center justify-center">
          <mascot type="ready_for_items" width="33%" min-width="250px" />
          <div class="mb-2">
            {{ $t("chronos.timetable.no_timetables_in_term") }}
          </div>
        </div>
      </template>
    </v-data-iterator>
  </div>
</template>

<style scoped>
.scrollable-list {
  height: 100%;
  overflow-y: scroll;
}
</style>
