<script>
import {defineComponent} from 'vue'
import TopMenuView from "../components/TopMenuView.vue";
import FooterView from "../components/FooterView.vue";
import {http_inst, number_format} from "../lib";
import {forEach, remove} from "lodash-es";

export default defineComponent({
  name: "BasketView",
  components: {FooterView, TopMenuView},
  data: () => ({
    cart_items: []
  }),
  computed: {
    total_money () {
      let total_value = 0

      forEach(this.cart_items, (value) => {
        total_value += value.price * value.cart_cnt
      });

      return total_value
    }
  },
  methods: {
    number_format,
    payment() {
      form.action = "/order";
      form.submit();
    },
    basket_delete(item) {
      if (confirm("장바구니에서 삭제하시겠습니까?")) {
        http_inst.delete('/api/carts/' + item.goods_code).then(result => {
          remove(this.cart_items, (n) => {
            return n.id === item.id
          })
        }).catch(error => {
          alert('서버에서 에러가 발생했습니다')
        })
      }
    },
    goods_quantity_adjuest(action, item) {
      if (action ===  'plus') {
        item.cart_cnt += 1;
      } else {
        if (item.cart_cnt > 1) {
          item.cart_cnt -= 1;
        } else {
          alert('최소 1개는 구매해야 합니다');
        }
      }

      http_inst.put('/api/carts/' + item.goods_code, {goods_cnt: item.cart_cnt}).catch(error => {
        alert('서버에서 에러가 발생했습니다')
      })
    }
  },
  mounted () {
    http_inst.get('/api/carts').then(result => {
      const response_data = result.data
      this.cart_items = response_data.data
    }).catch(error => {
      alert('장바구니 정보를 불러오는데 실패했습니다')
    })
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="container mb-3">
      <div class="card shopping-cart">
        <div class="card-header bg-dark text-light">
          <font-awesome-icon icon="fa-solid fa-shopping-cart" />
          장바구니
          <RouterLink :to="{name: 'goods_list'}" class="btn btn-outline-info btn-sm fa-pull-right">계속 쇼핑하기</RouterLink>
          <div class="clearfix"></div>
        </div>
        <div class="card-body">
          <form>
            <input type="hidden" name="delete_goods_id" value="">
            <!-- PRODUCT -->
            <div class="row mb-2" :key="index" v-for="(item, index) in cart_items">
              <div class="col-12 col-sm-12 col-md-2 text-center">
                <img class="img-responsive" :src="item.goods_photo_url" alt="preview" width="120" height="80">
              </div>
              <div class="col-12 text-sm-center col-sm-12 text-md-start col-md-6">
                <h4 class="product-name"><strong>{{ item.goods_name }}</strong></h4>
                <h4>
                  <small>{{ item.goods_description }}</small>
                </h4>
              </div>
              <div class="col-12 col-sm-12 text-sm-center col-md-4 text-md-end row">
                <div class="col-3 col-sm-3 col-md-6 text-md-end" style="padding-top: 5px">
                  <h6><strong>{{ number_format(item.price) }} <span class="text-muted">x</span></strong></h6>
                </div>
                <div class="col-4 col-sm-4 col-md-4">
                  <input type="hidden" name="goods_id" v-model="item.goods_code">
                  <div class="quantity">
                    <input type="button" value="+" class="plus" @click="goods_quantity_adjuest('plus', item)">
                    <input type="number" step="1" max="99" min="1" v-model="item.cart_cnt" title="Qty" class="qty"
                           size="4" name="quantity">
                    <input type="button" value="-" class="minus" @click="goods_quantity_adjuest('minus', item)">
                  </div>
                </div>
                <div class="col-2 col-sm-2 col-md-2 text-right">
                  <button type="button" class="btn btn-outline-danger btn-xs" @click="basket_delete(item)">
                    <font-awesome-icon icon="fa-solid fa-trash" />
                  </button>
                </div>
              </div>
            </div>
            <!-- END PRODUCT -->
          </form>
        </div>
        <div class="card-footer">
          <div class="fa-pull-right" style="margin: 10px">
            <a href="#" @click="payment" class="btn btn-success fa-pull-right">결제하기</a>
            <div class="fa-pull-right" style="margin: 5px">
              Total price: <b>{{ number_format(total_money) }}</b>
            </div>
          </div>
        </div>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>
.quantity {
    float: left;
    margin-right: 15px;
    background-color: #eee;
    position: relative;
    width: 80px;
    overflow: hidden
}

.quantity input {
    margin: 0;
    text-align: center;
    width: 15px;
    height: 15px;
    padding: 0;
    float: right;
    color: #000;
    font-size: 20px;
    border: 0;
    outline: 0;
    background-color: #F6F6F6
}

.quantity input.qty {
    position: relative;
    border: 0;
    width: 100%;
    height: 40px;
    padding: 10px 25px 10px 10px;
    text-align: center;
    font-weight: 400;
    font-size: 15px;
    border-radius: 0;
    background-clip: padding-box
}

.quantity .minus, .quantity .plus {
    line-height: 0;
    background-clip: padding-box;
    -webkit-border-radius: 0;
    -moz-border-radius: 0;
    border-radius: 0;
    -webkit-background-size: 6px 30px;
    -moz-background-size: 6px 30px;
    color: #bbb;
    font-size: 20px;
    position: absolute;
    height: 50%;
    border: 0;
    right: 0;
    padding: 0;
    width: 25px;
    z-index: 3
}

.quantity .minus:hover, .quantity .plus:hover {
    background-color: #dad8da
}

.quantity .minus {
    bottom: 0
}
.shopping-cart {
    margin-top: 20px;
}
</style>