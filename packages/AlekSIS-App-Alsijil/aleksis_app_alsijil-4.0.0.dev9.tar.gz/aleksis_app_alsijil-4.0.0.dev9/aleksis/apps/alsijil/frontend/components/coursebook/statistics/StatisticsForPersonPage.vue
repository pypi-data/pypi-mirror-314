<template>
  <fullscreen-dialog-page
    :fallback-url="{ name: 'core.personById', props: { id: personId } }"
  >
    <div class="d-flex" style="gap: 4em">
      <div class="flex-grow-1" style="max-width: 100%">
        <!-- documentations for person list -->
        <c-r-u-d-iterator
          i18n-key="alsijil.coursebook.statistics"
          :gql-query="gqlQuery"
          :gql-additional-query-args="gqlQueryArgs"
          :enable-create="false"
          :enable-edit="false"
          :elevated="false"
        >
          <template #additionalActions>
            <v-btn-toggle
              :value="mode"
              @change="updateMode"
              mandatory
              color="secondary"
              rounded
              dense
            >
              <v-btn outlined :value="MODE.PARTICIPATIONS">
                {{ $t("alsijil.coursebook.absences.absences") }}
              </v-btn>
              <v-btn outlined :value="MODE.PERSONAL_NOTES">
                {{ $t("alsijil.personal_notes.personal_notes") }}
              </v-btn>
            </v-btn-toggle>
            <v-btn
              v-if="$vuetify.breakpoint.mobile"
              rounded
              dense
              outlined
              text
              @click="statisticsBottomSheet = !statisticsBottomSheet"
            >
              {{ $t("alsijil.personal_notes.statistics.person_page.summary") }}
            </v-btn>
          </template>
          <template #default="{ items }">
            <v-list>
              <v-list-item v-for="item in items" :key="item.id" ripple>
                <v-list-item-content>
                  <v-list-item-title>
                    <!-- date & timeslot -->
                    <time
                      :datetime="item.relatedDocumentation.datetimeStart"
                      class="text-no-wrap"
                    >
                      {{
                        $d(
                          $parseISODate(
                            item.relatedDocumentation.datetimeStart,
                          ),
                          "short",
                        )
                      }}
                    </time>

                    <time
                      :datetime="item.relatedDocumentation.datetimeStart"
                      class="text-no-wrap"
                    >
                      {{
                        $d(
                          $parseISODate(
                            item.relatedDocumentation.datetimeStart,
                          ),
                          "shortTime",
                        )
                      }}
                    </time>
                    <span>-</span>
                    <time
                      :datetime="item.relatedDocumentation.datetimeEnd"
                      class="text-no-wrap"
                    >
                      {{
                        $d(
                          $parseISODate(item.relatedDocumentation.datetimeEnd),
                          "shortTime",
                        )
                      }}
                    </time>
                  </v-list-item-title>
                  <v-list-item-subtitle class="overflow-scroll">
                    <!-- teacher -->
                    <person-chip
                      v-for="teacher in item.relatedDocumentation.teachers"
                      :key="teacher.id"
                      :person="teacher"
                      no-link
                      small
                    />
                    <!-- group -->
                    <span>
                      {{ item.groupShortName }}
                    </span>
                    <!-- subject -->
                    <subject-chip
                      :subject="item.relatedDocumentation.subject"
                      small
                    />
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <!-- chips: absences & extraMarks -->
                  <absence-reason-chip
                    v-if="item.absenceReason"
                    :absence-reason="item.absenceReason"
                  />
                  <extra-mark-chip
                    v-if="item.extraMark"
                    :extra-mark="item.extraMark"
                  />
                  <div v-if="item.note">
                    {{ item.note }}
                  </div>
                </v-list-item-action>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
          </template>
        </c-r-u-d-iterator>
      </div>
      <statistics-for-person-card
        v-if="!$vuetify.breakpoint.mobile"
        class="flex-shrink-1"
        :compact="false"
        :person="{ id: personId }"
      />
      <v-bottom-sheet v-model="statisticsBottomSheet" v-else>
        <statistics-for-person-card
          :compact="false"
          :person="{ id: personId }"
        />
      </v-bottom-sheet>
    </div>
    <template #actions="{ toolbar }">
      <active-school-term-select
        v-if="toolbar"
        v-model="$root.activeSchoolTerm"
        color="secondary"
      />
      <!-- TODO: add functionality -->
      <v-btn v-if="toolbar" icon color="primary" disabled>
        <v-icon>$print</v-icon>
      </v-btn>
      <FabButton v-else icon-text="$print" i18n-key="actions.print" disabled />
    </template>
  </fullscreen-dialog-page>
</template>

<script>
import AbsenceReasonChip from "aleksis.apps.kolego/components/AbsenceReasonChip.vue";
import ActiveSchoolTermSelect from "aleksis.core/components/school_term/ActiveSchoolTermSelect.vue";
import CRUDIterator from "aleksis.core/components/generic/CRUDIterator.vue";
import FabButton from "aleksis.core/components/generic/buttons/FabButton.vue";
import FullscreenDialogPage from "aleksis.core/components/generic/dialogs/FullscreenDialogPage.vue";
import PersonChip from "aleksis.core/components/person/PersonChip.vue";
import SubjectChip from "aleksis.apps.cursus/components/SubjectChip.vue";
import StatisticsForPersonCard from "./StatisticsForPersonCard.vue";

import {
  participationsOfPerson,
  personalNotesForPerson,
  personName,
} from "./statistics.graphql";
import ExtraMarkChip from "../../extra_marks/ExtraMarkChip.vue";
import { MODE } from "./modes.js";

export default {
  name: "StatisticsForPersonPage",
  components: {
    ActiveSchoolTermSelect,
    ExtraMarkChip,
    AbsenceReasonChip,
    CRUDIterator,
    FabButton,
    FullscreenDialogPage,
    PersonChip,
    SubjectChip,
    StatisticsForPersonCard,
  },
  props: {
    // personId is supplied via the url
    personId: {
      type: [Number, String],
      required: true,
    },
    mode: {
      type: String,
      required: false,
      default: MODE.PARTICIPATIONS,
    },
  },
  apollo: {
    personName: {
      query: personName,
      variables() {
        return {
          person: this.personId,
        };
      },
      result({ data }) {
        this.$setToolBarTitle(
          this.$t("alsijil.coursebook.statistics.person_page.title", {
            fullName: data.personName.fullName || "???",
          }),
        );
      },
    },
  },
  data() {
    return {
      statisticsBottomSheet: false,
    };
  },
  computed: {
    gqlQueryArgs() {
      return {
        person: this.personId,
      };
    },
    MODE() {
      return MODE;
    },
  },
  methods: {
    gqlQuery() {
      return this.mode === MODE.PERSONAL_NOTES
        ? personalNotesForPerson
        : participationsOfPerson;
    },
    updateMode(mode = MODE.PARTICIPATIONS) {
      if (mode === this.mode) {
        return;
      }

      this.$router.push({
        name: "alsijil.coursebook_statistics",
        params: {
          personId: this.personId,
          mode: mode,
        },
      });
    },
  },
};
</script>
