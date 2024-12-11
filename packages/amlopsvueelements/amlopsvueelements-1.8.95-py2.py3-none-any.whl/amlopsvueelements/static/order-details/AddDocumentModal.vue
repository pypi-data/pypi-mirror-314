<template>
  <div v-if="isOpen" class="order-modal add-document-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes :is-modal="true">
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">Add Document</div>
                <button @click.stop="emit('modal-close')">
                  <img
                    width="12"
                    height="12"
                    src="../../assets/icons/cross.svg"
                    alt="delete"
                    class="close"
                  />
                </button>
              </div>
            </template>
            <template #content>
              <ScrollBar>
                <div class="form-body-wrapper">
                  <SelectField
                    v-model="entity"
                    label-text="Entity"
                    required
                    placeholder=""
                    label=""
                    :options="entities"
                  ></SelectField>
                  <!-- TO DO replace when type endpoint available -->
                  <SelectField
                    v-model="entity"
                    label-text="Type"
                    required
                    placeholder=""
                    label=""
                    :options="entities"
                  ></SelectField>
                  <div class="flex items-end gap-[1rem] mb-[1rem] w-full">
                    <div class="flex flex-col">
                      <Label :required="false" label-text="Valid From" />
                      <FlatPickr
                        v-model="date.from"
                        placeholder=""
                        :config="{
                          allowInput: true,
                          altInput: true,
                          altFormat: 'Y-m-d',
                          dateFormat: 'Y-m-d'
                        }"
                      />
                    </div>
                    <div class="flex flex-col">
                      <Label
                        :required="false"
                        label-text="Valid To"
                        :class="{ 'text-disabled': dateUFN }"
                      />
                      <FlatPickr
                        v-model="date.to"
                        :is-disabled="dateUFN"
                        placeholder=""
                        :config="{
                          allowInput: true,
                          altInput: true,
                          altFormat: 'Y-m-d',
                          dateFormat: 'Y-m-d'
                        }"
                      />
                    </div>
                    <div class="flex items-center mb-[0.5rem]">
                      <CheckboxField v-model="dateUFN" :size="'24px'" class="mb-0 mr-[0.25rem]" />
                      <p class="text-base whitespace-nowrap">UFN</p>
                    </div>
                  </div>
                  <InputField
                    v-model="name"
                    required
                    class="w-full mb-[1rem]"
                    label-text="Name"
                    placeholder="Please enter name"
                  />
                </div>
                <div class="flex items-center justify-start mb-[0.75rem] gap-3">
                  <button class="modal-button icon" @click="onFileInputClick()">
                    <img
                      height="20"
                      width="20"
                      :src="
                        file
                          ? getImageUrl('assets/icons/file.svg')
                          : getImageUrl('assets/icons/paperclip.svg')
                      "
                      alt="attachment"
                    />
                  </button>
                  <input
                    ref="fileInputAddDocument"
                    class="hidden"
                    type="file"
                    @change="onChangeFile($event)"
                  />
                  <p class="text-base whitespace-nowrap font-semibold text-main">
                    {{
                      (file! as File)?.name
                        ? (file! as File)?.name.split('.')[0].substring(0, 40) +
                          '.' +
                          (file! as File)?.name.split('.')[1]
                        : ' Select Document File'
                    }}
                  </p>
                </div>
              </ScrollBar>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Back</button>
          <button class="modal-button submit" @click.stop="onValidate()">Create Document</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { type Ref, ref, shallowRef, watch } from 'vue';
import { computed } from 'vue';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import { getImageUrl } from '@/helpers';
import FlatPickr from '../FlatPickr/FlatPickr.vue';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import Label from '../forms/Label.vue';
import ScrollBar from '../forms/ScrollBar.vue';

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['modal-close', 'modal-submit']);
const target = ref(null);

const orderStore = useOrderStore();
const order = computed(() => orderStore.order);
const entities = computed(() =>
  order.value?.tails?.length === 0
    ? [order.value?.client?.full_repr]
    : order.value?.tails?.map((el) => el.tail_number?.full_repr)
);
const entity: Ref<string> = shallowRef('');
const date = ref({
  from: '',
  to: ''
});
const dateUFN = shallowRef(false);
const name = shallowRef('');
const file = ref(null);
const fileInputAddDocument = ref(null);
const enabled = ref(false);

const onChangeFile = (event: any) => {
  const fileData = event.target.files[0];
  if (fileData) {
    file.value = fileData;
  }
};

const onFileInputClick = () => {
  (fileInputAddDocument.value! as HTMLElement).click();
};

const onValidate = async () => {
  emit('modal-submit');
  emit('modal-close');
};

watch(
  () => props.isOpen,
  (value) => {
    enabled.value = value;
  }
);

watch(
  () => dateUFN.value,
  (value) => {
    if (value) {
      date.value.to = '';
    }
  }
);
</script>

<style scoped lang="scss">
.add-document-modal {
  .modal-button {
    &.icon {
      background-color: rgba(240, 242, 252, 1);
      color: rgb(81 93 138);
      padding: 0.75rem;
      border-radius: 0.75rem;
      height: 100%;
    }
  }
}
</style>
