<template>
  <byjove-product :mode="mode">
    <template #extra-panels="productProps">

      <b-collapse class="card"
                  animation="slide"
                  :open="false"
                  aria-id="contentIdForFoo"
                  v-if="productProps.product">

        <template #trigger="props">
          <div class="card-header"
               role="button"
               aria-controls="contentIdForFoo"
               :aria-expanded="props.open">
            <p class="card-header-title">
              Foo
            </p>
            <a class="card-header-icon">
              <b-icon pack="fas"
                      :icon="props.open ? 'angle-down' : 'angle-up'">
              </b-icon>
            </a>
          </div>
        </template>

        <div class="card-content">
          <div class="content">
            <p>TODO: bar or baz</p>
          </div>
        </div>
      </b-collapse>

    </template>
  </byjove-product>
</template>

<script>
import {ByjoveProduct} from 'byjove'

export default {
    name: 'Product',
    components: {
        ByjoveProduct,
    },
    props: {
        mode: String,
    },
}
</script>
