<script>
import groupActionsMixin from "aleksis.core/components/group/actions/groupActionsMixin.js";
export default {
  name: "ShowAbsences",
  mixins: [groupActionsMixin],
};
</script>

<template>
  <v-list-item
    :to="{
      name: 'alsijil.coursebook',
      params: {
        filterType: 'all',
        pageType: 'absences',
        objType: 'group',
        objId: group.id,
      },
    }"
  >
    <v-list-item-icon>
      <v-icon>mdi-account-details-outline</v-icon>
    </v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title>
        {{ $t("actions.show_absences") }}
      </v-list-item-title>
    </v-list-item-content>
  </v-list-item>
</template>
