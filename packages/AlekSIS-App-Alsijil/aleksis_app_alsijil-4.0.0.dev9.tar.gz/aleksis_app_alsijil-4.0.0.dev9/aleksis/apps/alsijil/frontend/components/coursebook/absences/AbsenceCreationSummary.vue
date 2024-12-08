<template>
  <div>
    <message-box dense type="warning" class="mt-5">
      {{ $t("alsijil.coursebook.absences.warning") }}
    </message-box>
    <!-- MAYBE introduce a minimal variant of CRUDIterator -->
    <!--       with most features disabled for this list usecase -->
    <c-r-u-d-iterator
      i18n-key=""
      :gql-query="gqlQuery"
      :gql-additional-query-args="gqlArgs"
      :enable-search="false"
      :enable-create="false"
      :enable-edit="false"
      :elevated="false"
      disable-pagination
      hide-default-footer
      @loading="handleLoading"
    >
      <template #default="{ items }">
        <v-expansion-panels>
          <v-expansion-panel v-for="person in items" :key="person.id">
            <v-expansion-panel-header>
              <div>
                {{ persons.find((p) => p.id === person.id).fullName }}
              </div>
              <v-spacer />
              <div>
                {{
                  $tc(
                    "alsijil.coursebook.absences.lessons",
                    person.lessons.length,
                    { count: person.lessons.length },
                  )
                }}
              </div>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-list-item
                v-for="lesson in person.lessons"
                class="px-0"
                :key="lesson.id"
              >
                <v-row>
                  <!-- TODO: We should extract this display & share it -->
                  <v-col cols="3">
                    <time :datetime="lesson.datetimeStart" class="text-no-wrap">
                      {{
                        $d(
                          $parseISODate(lesson.datetimeStart),
                          "shortWithWeekday",
                        )
                      }}&nbsp;
                    </time>
                  </v-col>
                  <v-col cols="3">
                    <time :datetime="lesson.datetimeStart" class="text-no-wrap">
                      {{ $d($parseISODate(lesson.datetimeStart), "shortTime") }}
                    </time>
                    <span> - </span>
                    <time :datetime="lesson.datetimeEnd" class="text-no-wrap">
                      {{ $d($parseISODate(lesson.datetimeEnd), "shortTime") }}
                    </time>
                  </v-col>
                  <v-col cols="3">
                    {{ lesson.course?.name }}
                  </v-col>
                  <v-col cols="3">
                    <subject-chip :subject="lesson.subject" />
                  </v-col>
                </v-row>
              </v-list-item>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </template>
    </c-r-u-d-iterator>
  </div>
</template>

<script>
import CRUDIterator from "aleksis.core/components/generic/CRUDIterator.vue";
import SubjectChip from "aleksis.apps.cursus/components/SubjectChip.vue";
import { lessonsForPersons } from "./absenceCreation.graphql";
import loadingMixin from "aleksis.core/mixins/loadingMixin.js";

export default {
  name: "AbsenceCreationSummary",
  components: {
    CRUDIterator,
    SubjectChip,
  },
  mixins: [loadingMixin],
  props: {
    persons: {
      type: Array,
      required: true,
    },
    startDate: {
      type: String,
      required: true,
    },
    endDate: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      gqlQuery: lessonsForPersons,
    };
  },
  computed: {
    gqlArgs() {
      return {
        persons: this.persons.map((person) => person.id),
        start: this.startDate,
        end: this.endDate,
      };
    },
  },
};
</script>
