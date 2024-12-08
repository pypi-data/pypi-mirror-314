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
import documentationPartMixin from "./documentationPartMixin";

import { DateTime } from "luxon";

export default {
  name: "DocumentationStatus",
  mixins: [documentationPartMixin],
  data() {
    return {
      statusChoices: [
        {
          name: "available",
          text: this.$t("alsijil.coursebook.status.available"),
          icon: "$success",
          color: "success",
        },
        {
          name: "missing",
          text: this.$t("alsijil.coursebook.status.missing"),
          icon: "$warning",
          color: "error",
        },
        {
          name: "running",
          text: this.$t("alsijil.coursebook.status.running"),
          icon: "mdi-play-outline",
          color: "warning",
        },
        {
          name: "substitution",
          text: this.$t("alsijil.coursebook.status.substitution"),
          icon: "$info",
          color: "warning",
        },
        {
          name: "cancelled",
          text: this.$t("alsijil.coursebook.status.cancelled"),
          icon: "mdi-cancel",
          color: "error",
        },
        {
          name: "pending",
          text: this.$t("alsijil.coursebook.status.pending"),
          icon: "mdi-clipboard-clock-outline",
          color: "blue",
        },
      ],
      statusTimeout: null,
      currentStatusName: "",
    };
  },
  computed: {
    currentStatus() {
      return this.statusChoices.find((s) => s.name === this.currentStatusName);
    },
    documentationDateTimeStart() {
      return DateTime.fromISO(this.documentation.datetimeStart);
    },
    documentationDateTimeEnd() {
      return DateTime.fromISO(this.documentation.datetimeEnd);
    },
  },
  methods: {
    updateStatus() {
      if (this.documentation?.amends.cancelled) {
        this.currentStatusName = "cancelled";
      } else if (this.documentation.topic) {
        this.currentStatusName = "available";
      } else if (DateTime.now() > this.documentationDateTimeEnd) {
        this.currentStatusName = "missing";
      } else if (this.documentation?.amends.amends) {
        this.currentStatusName = "substitution";
      } else if (
        DateTime.now() > this.documentationDateTimeStart &&
        DateTime.now() < this.documentationDateTimeEnd
      ) {
        this.currentStatusName = "running";
      } else {
        this.currentStatusName = "pending";
      }
    },
  },
  watch: {
    documentation: {
      handler() {
        this.updateStatus();
      },
      deep: true,
    },
  },
  mounted() {
    this.updateStatus();

    if (DateTime.now() < this.documentationDateTimeStart) {
      this.statusTimeout = setTimeout(
        this.updateStatus,
        this.documentationDateTimeStart
          .diff(DateTime.now(), "seconds")
          .toObject(),
      );
    } else if (DateTime.now() < this.documentationDateTimeEnd) {
      this.statusTimeout = setTimeout(
        this.updateStatus,
        this.documentationDateTimeEnd
          .diff(DateTime.now(), "seconds")
          .toObject(),
      );
    }
  },
  beforeDestroy() {
    if (this.statusTimeout) {
      clearTimeout(this.statusTimeout);
    }
  },
};
</script>
