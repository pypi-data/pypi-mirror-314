<script>
import groupActionsMixin from "aleksis.core/components/group/actions/groupActionsMixin.js";
export default {
  name: "OpenCoursebook",
  mixins: [groupActionsMixin],
};
</script>

<template>
  <v-list-item
    :to="{
      name: 'alsijil.coursebook',
      params: {
        filterType: 'all',
        pageType: 'documentations',
        objType: 'group',
        objId: group.id,
      },
    }"
  >
    <v-list-item-icon>
      <v-icon>mdi-book-education-outline</v-icon>
    </v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title>
        {{ $t("actions.open_in_coursebook") }}
      </v-list-item-title>
    </v-list-item-content>
  </v-list-item>
</template>
