<script>
import { gqlAvailableTimetables } from "./timetables.graphql";
import NoTimetableCard from "./NoTimetableCard.vue";
import SelectTimetable from "./SelectTimetable.vue";
import timetableTypes from "./timetableTypes";

export default {
  name: "TimetableWrapper",
  components: { NoTimetableCard, SelectTimetable },
  apollo: {
    availableTimetables: {
      query: gqlAvailableTimetables,
      result() {
        if (
          !this.selected &&
          this.$route.params.id &&
          this.$route.params.type
        ) {
          this.selectTimetable(
            this.availableTimetables.find(
              (t) =>
                t.objId === this.$route.params.id &&
                t.type.toLowerCase() === this.$route.params.type,
            ),
          );
        }
      },
    },
  },
  data() {
    return {
      availableTimetables: [],
      selected: null,
      search: "",
      selectedTypes: ["GROUP", "TEACHER", "ROOM"],
      types: timetableTypes,
      selectDialog: false,
    };
  },
  props: {
    onSelected: {
      type: Function,
      required: false,
      default: null,
    },
  },
  watch: {
    selected(selected) {
      if (this.onSelected) {
        this.onSelected(selected);
        return;
      }
      // Align navigation with currently selected timetable
      if (!selected) {
        this.$router.push({ name: "chronos.timetable" });
      } else if (
        selected.objId !== this.$route.params.id ||
        selected.type.toLowerCase() !== this.$route.params.type
      ) {
        this.$router.push({
          name: "chronos.timetableWithId",
          params: {
            type: selected.type.toLowerCase(),
            id: selected.objId,
          },
        });
      }
    },
  },
  methods: {
    findNextTimetable(offset = 1) {
      const currentIndex = this.availableTimetablesIds.indexOf(
        this.selected.id,
      );
      const newIndex = currentIndex + offset;
      if (newIndex < 0 || newIndex >= this.availableTimetablesIds.length) {
        return null;
      }
      return this.availableTimetables[newIndex];
    },
    selectTimetable(timetable) {
      this.selected = timetable;
    },
  },
  computed: {
    selectedTypesFull() {
      return this.selectedTypes.map((type) => {
        return this.types[type];
      });
    },
    availableTimetablesFiltered() {
      // Filter timetables by selected types
      return this.availableTimetables.filter((timetable) => {
        return this.selectedTypes.indexOf(timetable.type) !== -1;
      });
    },
    availableTimetablesIds() {
      return this.availableTimetables.map((timetable) => timetable.id);
    },
    prevTimetable() {
      return this.findNextTimetable(-1);
    },
    nextTimetable() {
      return this.findNextTimetable(1);
    },
  },
};
</script>

<template>
  <div>
    <v-row>
      <v-dialog
        v-model="selectDialog"
        fullscreen
        hide-overlay
        transition="dialog-bottom-transition"
      >
        <v-card>
          <v-toolbar dark color="primary">
            <v-btn icon dark @click="selectDialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>{{
              $t("chronos.timetable.select")
            }}</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <slot
            name="additionalSelect"
            :selected="selected"
            :mobile="true"
          ></slot>
          <select-timetable
            v-model="selected"
            @input="selectDialog = false"
            :loading="$apollo.queries.availableTimetables.loading"
            :available-timetables="availableTimetables"
          />
        </v-card>
      </v-dialog>

      <v-col md="3" lg="3" xl="3" v-if="$vuetify.breakpoint.lgAndUp">
        <slot
          name="additionalSelect"
          :selected="selected"
          :mobile="false"
        ></slot>
        <v-card>
          <select-timetable
            v-model="selected"
            :loading="$apollo.queries.availableTimetables.loading"
            :available-timetables="availableTimetables"
            limit-height
          />
        </v-card>
      </v-col>
      <v-col sm="12" md="12" lg="9" xl="9" class="full-height">
        <!-- No timetable card-->
        <no-timetable-card
          v-if="selected == null"
          @selectTimetable="selectDialog = true"
        />

        <!-- Calendar card-->
        <v-card v-else>
          <div class="d-flex flex-column" v-if="$vuetify.breakpoint.mdAndDown">
            <v-card-title class="pt-2">
              <v-btn
                icon
                :disabled="!prevTimetable"
                @click="selectTimetable(prevTimetable)"
                :title="$t('chronos.timetable.prev')"
                class="mr-1"
              >
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>
              <v-spacer />
              <v-chip outlined color="secondary" @click="selectDialog = true">
                {{ selected.name }}
                <v-icon right>mdi-chevron-down</v-icon>
              </v-chip>
              <v-spacer />
              <v-btn
                icon
                :disabled="!nextTimetable"
                @click="selectTimetable(nextTimetable)"
                :title="$t('chronos.timetable.next')"
                class="ml-1 float-right"
              >
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </v-card-title>
            <slot
              name="additionalButton"
              :selected="selected"
              :mobile="true"
            ></slot>
          </div>

          <div class="d-flex flex-wrap justify-space-between mb-2" v-else>
            <v-card-title>
              {{ selected.name }}
              <slot
                name="additionalButton"
                :selected="selected"
                :mobile="false"
              ></slot>
            </v-card-title>
            <div class="pa-2 mt-1">
              <v-btn
                icon
                :disabled="!prevTimetable"
                @click="selectTimetable(prevTimetable)"
                :title="$t('chronos.timetable.prev')"
              >
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>
              <v-chip label color="secondary" outlined class="mx-1">{{
                selected.shortName
              }}</v-chip>
              <v-btn
                icon
                :disabled="!nextTimetable"
                @click="selectTimetable(nextTimetable)"
                :title="$t('chronos.timetable.next')"
              >
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </div>
          </div>
          <slot :selected="selected"></slot>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
