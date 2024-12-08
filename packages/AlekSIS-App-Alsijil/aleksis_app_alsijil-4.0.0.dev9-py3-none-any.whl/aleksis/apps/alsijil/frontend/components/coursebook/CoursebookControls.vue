<script setup>
import CoursebookPrintDialog from "./CoursebookPrintDialog.vue";
</script>

<template>
  <div
    class="d-flex flex-column flex-sm-row flex-nowrap flex-grow-1 justify-end gap align-stretch"
  >
    <v-autocomplete
      :items="selectable"
      item-text="name"
      :item-value="(item) => `${item.__typename}-${item.id}`"
      clearable
      return-object
      filled
      dense
      hide-details
      :placeholder="$t('alsijil.coursebook.filter.filter_for_obj')"
      :loading="selectLoading"
      :value="currentObj"
      @input="selectObject"
      @click:clear="selectObject"
      class="max-width"
    />
    <div class="mx-6">
      <v-switch
        :loading="selectLoading"
        :label="$t('alsijil.coursebook.filter.own')"
        :input-value="value.filterType === 'my'"
        @change="selectFilterType($event)"
        dense
        inset
        hide-details
      />
      <v-switch
        :loading="selectLoading"
        :label="$t('alsijil.coursebook.filter.missing')"
        :input-value="value.incomplete"
        @change="
          $emit('input', {
            incomplete: $event,
          })
        "
        dense
        inset
        hide-details
      />
      <v-switch
        v-if="pageType === 'absences'"
        :loading="selectLoading"
        :label="$t('alsijil.coursebook.filter.absences_exist')"
        :input-value="value.absencesExist"
        @change="
          $emit('input', {
            absencesExist: $event,
          })
        "
        dense
        inset
        hide-details
      />
    </div>
    <div class="d-flex flex-column gap">
      <v-btn
        outlined
        color="primary"
        :loading="selectLoading"
        @click="togglePageType()"
      >
        {{ pageTypeButtonText }}
      </v-btn>
      <coursebook-print-dialog
        v-if="pageType === 'documentations'"
        :loading="selectLoading"
        :available-groups="groups"
        :value="currentGroups"
      />
    </div>
  </div>
</template>

<script>
import { coursesOfPerson, groupsByPerson } from "./coursebook.graphql";

const TYPENAMES_TO_TYPES = {
  CourseType: "course",
  GroupType: "group",
};
export default {
  name: "CoursebookFilters",
  data() {
    return {
      // Placeholder values while query isn't completed yet
      groups: [],
      courses: [],
    };
  },
  props: {
    value: {
      type: Object,
      required: true,
    },
    pageType: {
      type: String,
      required: false,
      default: "documentations",
    },
  },
  emits: ["input"],
  apollo: {
    groups: {
      query: groupsByPerson,
    },
    courses: {
      query: coursesOfPerson,
    },
  },
  computed: {
    selectable() {
      return [
        { header: this.$t("alsijil.coursebook.filter.groups") },
        ...this.groups,
        { header: this.$t("alsijil.coursebook.filter.courses") },
        ...this.courses,
      ];
    },
    selectLoading() {
      return (
        this.$apollo.queries.groups.loading ||
        this.$apollo.queries.courses.loading
      );
    },
    currentObj() {
      return this.selectable.find(
        (o) =>
          TYPENAMES_TO_TYPES[o.__typename] === this.value.objType &&
          o.id === this.value.objId,
      );
    },
    currentGroups() {
      return this.groups.filter(
        (o) =>
          TYPENAMES_TO_TYPES[o.__typename] === this.value.objType &&
          o.id === this.value.objId,
      );
    },
    pageTypeButtonText() {
      if (this.value.pageType === "documentations") {
        return this.$t("alsijil.coursebook.filter.page_type.absences");
      } else {
        return this.$t("alsijil.coursebook.filter.page_type.documentations");
      }
    },
  },
  methods: {
    selectObject(selection) {
      this.$emit("input", {
        objType: selection ? TYPENAMES_TO_TYPES[selection.__typename] : null,
        objId: selection ? selection.id : null,
      });
    },
    selectFilterType(switchValue) {
      this.$emit("input", {
        filterType: switchValue ? "my" : "all",
        objType: this.value.objType,
        objId: this.value.objId,
      });
    },
    togglePageType() {
      this.$emit("input", {
        pageType:
          this.value.pageType === "documentations"
            ? "absences"
            : "documentations",
        objType: this.value.objType,
        objId: this.value.objId,
      });
    },
  },
};
</script>
