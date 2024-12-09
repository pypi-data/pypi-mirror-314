/**
 * Mixin with common used API for custom lesson event calendar components
 */
const lessonEvent = {
  methods: {
    addStatuses(attr) {
      let oldItems = this.getOldItems(attr);
      let newItems = this.getNewItems(attr);
      let oldIds = oldItems.map((item) => item.id);
      let newIds = newItems.map((item) => item.id);
      let itemsWithStatus = oldItems.concat(newItems).map((item) => {
        let status = "regular";
        if (newIds.includes(item.id) && !oldIds.includes(item.id)) {
          status = "new";
        } else if (
          newIds.length > 0 &&
          !newIds.includes(item.id) &&
          oldIds.includes(item.id)
        ) {
          status = "removed";
        }
        return { ...item, status: status };
      });
      return itemsWithStatus;
    },
    getOldItems(attr) {
      let oldItems = [];
      if (this.selectedEvent.meta.amended) {
        oldItems = this.selectedEvent.meta.amends[attr];
      } else {
        oldItems = this.selectedEvent.meta[attr];
      }
      return oldItems;
    },
    getNewItems(attr) {
      let newItems = [];
      if (this.selectedEvent.meta.amended) {
        newItems = this.selectedEvent.meta[attr];
      }
      return newItems;
    },
  },
  computed: {
    teachers() {
      return this.addStatuses("teachers");
    },
    oldTeachers() {
      return this.getOldItems("teachers");
    },
    newTeachers() {
      return this.getNewItems("teachers");
    },

    rooms() {
      return this.addStatuses("rooms");
    },
    oldRooms() {
      return this.getOldItems("rooms");
    },
    newRooms() {
      return this.getNewItems("rooms");
    },
    currentSubject() {
      if (this.selectedEvent.meta.subject) {
        return this.selectedEvent.meta.subject;
      } else if (
        this.selectedEvent.meta.amended &&
        this.selectedEvent.meta.amends.subject
      ) {
        return this.selectedEvent.meta.amends.subject;
      } else {
        return null;
      }
    },
  },
};

export default lessonEvent;
