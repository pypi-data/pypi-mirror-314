<template>
  <div>
    <infinite-scrolling-date-sorted-c-r-u-d-iterator
      i18n-key="alsijil.coursebook"
      :gql-query="gqlQuery"
      :gql-additional-query-args="gqlQueryArgs"
      :enable-create="false"
      :enable-edit="false"
      :elevated="false"
      @lastQuery="lastQuery = $event"
      ref="iterator"
      fixed-header
      disable-pagination
      hide-default-footer
      use-deep-search
    >
      <template #additionalActions="{ attrs, on }">
        <coursebook-controls :page-type="pageType" v-model="filters" />
        <v-expand-transition>
          <v-card
            outlined
            class="full-width"
            v-show="
              pageType === 'absences' && combinedSelectedParticipations.length
            "
          >
            <v-card-text>
              <v-row align="center">
                <v-col cols="6">
                  {{
                    $tc(
                      "alsijil.coursebook.absences.action_for_selected",
                      combinedSelectedParticipations.length,
                    )
                  }}
                </v-col>
                <v-col cols="6">
                  <absence-reason-buttons
                    allow-empty
                    empty-value="present"
                    :custom-absence-reasons="absenceReasons"
                    @input="handleMultipleAction"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-expand-transition>
      </template>

      <template #item="{ item, lastQuery }">
        <component
          :is="itemComponent"
          :extra-marks="extraMarks"
          :absence-reasons="absenceReasons"
          :subjects="subjects"
          :documentation="item"
          :affected-query="lastQuery"
          :value="selectedParticipations[item.id] ??= []"
          @input="selectParticipation(item.id, $event)"
        />
      </template>

      <template #loading>
        <coursebook-loader :number-of-days="10" :number-of-docs="5" />
      </template>

      <template #itemLoader>
        <DocumentationLoader />
      </template>
    </infinite-scrolling-date-sorted-c-r-u-d-iterator>
    <absence-creation-dialog :absence-reasons="absenceReasons" />
  </div>
</template>

<script>
import InfiniteScrollingDateSortedCRUDIterator from "aleksis.core/components/generic/InfiniteScrollingDateSortedCRUDIterator.vue";
import { documentationsForCoursebook } from "./coursebook.graphql";
import AbsenceReasonButtons from "aleksis.apps.kolego/components/AbsenceReasonButtons.vue";
import CoursebookControls from "./CoursebookControls.vue";
import CoursebookLoader from "./CoursebookLoader.vue";
import DocumentationModal from "./documentation/DocumentationModal.vue";
import DocumentationAbsencesModal from "./absences/DocumentationAbsencesModal.vue";
import AbsenceCreationDialog from "./absences/AbsenceCreationDialog.vue";
import { extraMarks } from "./queries/extraMarks.graphql";
import DocumentationLoader from "./documentation/DocumentationLoader.vue";
import sendToServerMixin from "./absences/sendToServerMixin";
import { absenceReasons } from "./queries/absenceReasons.graphql";
import { subjects } from "./queries/subjects.graphql";

export default {
  name: "Coursebook",
  components: {
    DocumentationLoader,
    AbsenceReasonButtons,
    CoursebookControls,
    CoursebookLoader,
    DocumentationModal,
    DocumentationAbsencesModal,
    InfiniteScrollingDateSortedCRUDIterator,
    AbsenceCreationDialog,
  },
  mixins: [sendToServerMixin],
  props: {
    filterType: {
      type: String,
      required: true,
    },
    objId: {
      type: [Number, String],
      required: false,
      default: null,
    },
    objType: {
      type: String,
      required: false,
      default: null,
    },
    pageType: {
      type: String,
      required: false,
      default: "documentations",
    },
    /**
     * Number of consecutive to load at once
     * This number of days is initially loaded and loaded
     * incrementally while scrolling.
     */
    dayIncrement: {
      type: Number,
      required: false,
      default: 7,
    },
    /**
     * Margin from coursebook list to top of viewport in pixels
     */
    topMargin: {
      type: Number,
      required: false,
      default: 165,
    },
  },
  data() {
    return {
      gqlQuery: documentationsForCoursebook,
      lastQuery: null,
      dateStart: "",
      dateEnd: "",
      // Placeholder values while query isn't completed yet
      groups: [],
      courses: [],
      incomplete: false,
      absencesExist: true,
      ready: false,
      initDate: false,
      currentDate: "",
      hashUpdater: false,
      extraMarks: [],
      absenceReasons: [],
      subjects: [],
      selectedParticipations: {},
    };
  },
  apollo: {
    extraMarks: {
      query: extraMarks,
      update: (data) => data.items,
    },
    absenceReasons: {
      query: absenceReasons,
      update: (data) => data.items,
    },
    subjects: {
      query: subjects,
      update: (data) => data.items,
    },
  },
  computed: {
    // Assertion: Should only fire on page load or selection change.
    //            Resets date range.
    gqlQueryArgs() {
      return {
        own: this.filterType === "all" ? false : true,
        objId: this.objId ? Number(this.objId) : undefined,
        objType: this.objType?.toUpperCase(),
        dateStart: this.dateStart,
        dateEnd: this.dateEnd,
        incomplete: !!this.incomplete,
        absencesExist: !!this.absencesExist && this.pageType === "absences",
      };
    },
    filters: {
      get() {
        return {
          objType: this.objType,
          objId: this.objId,
          filterType: this.filterType,
          incomplete: this.incomplete,
          pageType: this.pageType,
          absencesExist: this.absencesExist,
        };
      },
      set(selectedFilters) {
        if (Object.hasOwn(selectedFilters, "incomplete")) {
          this.incomplete = selectedFilters.incomplete;
        } else if (Object.hasOwn(selectedFilters, "absencesExist")) {
          this.absencesExist = selectedFilters.absencesExist;
        } else if (
          Object.hasOwn(selectedFilters, "filterType") ||
          Object.hasOwn(selectedFilters, "objId") ||
          Object.hasOwn(selectedFilters, "objType") ||
          Object.hasOwn(selectedFilters, "pageType")
        ) {
          this.$router.push({
            name: "alsijil.coursebook",
            params: {
              filterType: selectedFilters.filterType
                ? selectedFilters.filterType
                : this.filterType,
              objType: selectedFilters.objType,
              objId: selectedFilters.objId,
              pageType: selectedFilters.pageType
                ? selectedFilters.pageType
                : this.pageType,
            },
            hash: this.$route.hash,
          });
          // computed should not have side effects
          // but this was actually done before filters was refactored into
          // its own component
          this.$refs.iterator.resetDate();
          // might skip query until both set = atomic
          if (Object.hasOwn(selectedFilters, "pageType")) {
            this.absencesExist = true;
            this.$setToolBarTitle(
              this.$t(`alsijil.coursebook.title_${selectedFilters.pageType}`),
              null,
            );
          }
        }
      },
    },
    itemComponent() {
      if (this.pageType === "documentations") {
        return "DocumentationModal";
      } else {
        return "DocumentationAbsencesModal";
      }
    },
    combinedSelectedParticipations() {
      return Object.values(this.selectedParticipations).flat();
    },
  },
  methods: {
    selectParticipation(id, value) {
      this.selectedParticipations = Object.assign(
        {},
        this.selectedParticipations,
        { [id]: value },
      );
    },
    handleMultipleAction(absenceReasonId) {
      this.loadSelectedParticiptions = true;
      this.sendToServer(
        this.combinedSelectedParticipations,
        "absenceReason",
        absenceReasonId,
      );
      this.$once("save", this.resetMultipleAction);
    },
    resetMultipleAction() {
      this.loadSelectedParticiptions = false;
      this.selectedParticipations = {};
    },
  },
  mounted() {
    this.$setToolBarTitle(
      this.$t(`alsijil.coursebook.title_${this.pageType}`),
      null,
    );
  },
};
</script>

<style>
.max-width {
  max-width: 25rem;
}
</style>
