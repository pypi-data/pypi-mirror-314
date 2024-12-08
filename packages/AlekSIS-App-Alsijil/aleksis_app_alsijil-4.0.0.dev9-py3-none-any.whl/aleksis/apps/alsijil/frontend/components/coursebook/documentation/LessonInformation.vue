<script setup>
import DocumentationStatus from "./DocumentationStatus.vue";
import PersonChip from "aleksis.core/components/person/PersonChip.vue";
import SubjectChip from "aleksis.apps.cursus/components/SubjectChip.vue";
import SubjectChipSelectField from "aleksis.apps.cursus/components/SubjectChipSelectField.vue";
</script>

<template>
  <div :class="{ 'full-width grid': true, 'large-grid': largeGrid }">
    <div class="d-flex">
      <documentation-status v-if="compact" v-bind="documentationPartProps" />
      <div
        v-if="documentation.amends?.slotNumberStart"
        :class="{
          'text-h5 mr-3 d-flex flex-column justify-center slot-number': true,
          'ml-2 slot-number-mobile': !largeGrid,
        }"
      >
        <span
          v-if="
            documentation.amends?.slotNumberStart ==
            documentation.amends?.slotNumberEnd
          "
        >
          {{ documentation.amends?.slotNumberStart }}.
        </span>
        <span v-else>
          {{ documentation.amends?.slotNumberStart }}.–{{
            documentation.amends?.slotNumberEnd
          }}.
        </span>
      </div>
      <div :class="{ 'text-right d-flex flex-column fit-content': largeGrid }">
        <time :datetime="documentation.datetimeStart" class="text-no-wrap">
          {{ $d(toDateTime(documentation.datetimeStart), "shortTime") }}
        </time>
        <span v-if="!largeGrid">–</span>
        <time :datetime="documentation.datetimeEnd" class="text-no-wrap">
          {{ $d(toDateTime(documentation.datetimeEnd), "shortTime") }}
        </time>
      </div>
    </div>
    <span
      :class="{
        'text-right': !largeGrid,
        'text-subtitle-1': largeGrid,
        'font-weight-medium': largeGrid,
      }"
    >
      {{
        documentation.course?.name ||
        documentation.amends.title ||
        documentation.amends.amends.title
      }}
    </span>
    <div
      :class="{
        'd-flex align-center flex-wrap gap': true,
        'justify-center': largeGrid,
        'justify-start': !largeGrid,
      }"
    >
      <template v-if="documentation.subject">
        <subject-chip-select-field
          v-if="documentation.canEdit"
          :items="subjects"
          :value="documentation.subject"
          :disabled="loading"
          :loading="loading"
          @input="editSubject"
        />
        <subject-chip
          v-else
          :subject="documentation.subject"
          :disabled="loading"
        />
      </template>
      <subject-chip
        v-if="
          documentation?.amends?.amends?.subject &&
          documentation.amends.amends.subject.id !== documentation.subject.id
        "
        :subject="documentation.amends.amends.subject"
        v-bind="compact ? dialogActivator.attrs : {}"
        v-on="compact ? dialogActivator.on : {}"
        class="text-decoration-line-through"
        disabled
      />
    </div>
    <div
      :class="{
        'd-flex align-center flex-wrap gap': true,
        'justify-end': !largeGrid,
      }"
    >
      <person-chip
        v-for="teacher in documentation.teachers"
        :key="documentation.id + '-teacher-' + teacher.id"
        :person="teacher"
        :no-link="compact"
        v-bind="compact ? dialogActivator.attrs : {}"
        v-on="compact ? dialogActivator.on : {}"
      />
      <person-chip
        v-for="teacher in amendedTeachers"
        :key="documentation.id + '-amendedTeacher-' + teacher.id"
        :person="teacher"
        :no-link="compact"
        v-bind="compact ? dialogActivator.attrs : {}"
        v-on="compact ? dialogActivator.on : {}"
        class="text-decoration-line-through"
        disabled
      />
    </div>
  </div>
</template>

<script>
import { DateTime } from "luxon";

import createOrPatchMixin from "aleksis.core/mixins/createOrPatchMixin.js";

import documentationPartMixin from "./documentationPartMixin";
import documentationCacheUpdateMixin from "./documentationCacheUpdateMixin";

export default {
  name: "LessonInformation",
  mixins: [
    createOrPatchMixin,
    documentationCacheUpdateMixin,
    documentationPartMixin,
  ],
  methods: {
    toDateTime(dateString) {
      return DateTime.fromISO(dateString);
    },
    editSubject(subject) {
      this.createOrPatch([
        {
          id: this.documentation.id,
          subject: subject.id,
        },
      ]);
    },
  },
  computed: {
    largeGrid() {
      return this.compact && !this.$vuetify.breakpoint.mobile;
    },
    amendedTeachers() {
      if (
        this.documentation?.amends?.amends?.teachers &&
        this.documentation.amends.amends.teachers.length
      ) {
        return this.documentation.amends.amends.teachers.filter(
          (at) => !this.documentation.teachers.includes((t) => t.id === at.id),
        );
      }
      return [];
    },
  },
};
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 1em;
  align-content: start;
}

.large-grid {
  grid-template-columns: 1fr 1fr 1fr 1fr;
  align-content: unset;
}

.grid:last-child {
  justify-self: end;
  justify-content: end;
}

.fit-content {
  width: fit-content;
}

.gap {
  gap: 0.25em;
}

.slot-number {
  font-size: 1.6rem !important;
  font-weight: 300;
  line-height: 1.6rem;
}

.slot-number-mobile {
  font-size: 1.4rem !important;
  line-height: 1.4rem;
}
</style>
