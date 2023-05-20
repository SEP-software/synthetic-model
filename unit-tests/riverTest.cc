#include <gtest/gtest.h>  // googletest header file
#include <iostream>
#include <string>
#include "store.h"
using std::string;
using namespace SEP::IO;

TEST(createObjects, storage) {
  ASSERT_NO_THROW(returnStorage(SEP::DATA_BYTE, 4));
  ASSERT_NO_THROW(returnStorage(SEP::DATA_INT, 4));
  ASSERT_NO_THROW(returnStorage(SEP::DATA_FLOAT, 4));
  ASSERT_NO_THROW(returnStorage(SEP::DATA_DOUBLE, 4));
  ASSERT_NO_THROW(returnStorage(SEP::DATA_COMPLEX, 4));
}
class data4D {
 public:
  data4D(const int n1, const int n2, const int n3, const int n4) {
    nb.resize(7);
    std::vector<int> vec(n1 * n2 * n3 * n4);
    nb[0] = 1;
    nb[1] = n1;
    nb[2] = n1 * n2;
    nb[3] = n1 * n2 * n3;
    nb[4] = nb[5] = nb[6] = n1 * n2 * n3 * n4;
    size_t i = 0;
    for (int i4 = 0; i4 < n4; i4++) {
      for (int i3 = 0; i3 < n3; i3++) {
        for (int i2 = 0; i2 < n2; i2++) {
          for (int i1 = 0; i1 < n1; i1++, i++) {
            vec[i] = i1 + i2 * 100 + i3 * 10000 + i4 * 1000000;
          }
        }
      }
    }
    void *x = (void *)vec.data();
    store = std::make_shared<storeInt>(n1 * n2 * n3 * n4, x);
  }
  std::vector<int> nb;
  std::shared_ptr<storeInt> store;
};

TEST(sizeZero, storage) {
  data4D x(20, 20, 20, 20);
  EXPECT_EQ(x.store->getSize(), 20 * 20 * 20 * 20);
  x.store->zero();
  EXPECT_EQ(x.store->getSize(), 0);
}

TEST(checkSetGetPtr, storage) {
  data4D x(20, 20, 20, 20);
  int *y = (int *)x.store->getPtr();

  for (int i4 = 0; i4 < 20; i4++) {
    EXPECT_EQ(y[i4 * 20 * 20 * 20], 100 * 100 * 100 * i4);
    ;
  }
}
TEST(checkClone, storage) {
  data4D x(20, 20, 20, 20);

  std::shared_ptr<storeBase> z = x.store->clone();
  std::shared_ptr<storeInt> zz = std::dynamic_pointer_cast<storeInt>(z);
  int *y = (int *)zz->getPtr();

  for (int i4 = 0; i4 < 20; i4++) {
    EXPECT_EQ(y[i4 * 20 * 20 * 20], 100 * 100 * 100 * i4);
    ;
  }
}
TEST(checkGet, storage) {
  data4D x(20, 20, 20, 20);

  std::shared_ptr<storeBase> z = x.store->clone();
  int *y = (int *)z->getPtr();
  for (auto i = 0; i < 20 * 20 * 20 * 20; i++) y[i] = 0;
  x.store->getData(z);

  y = (int *)x.store->getPtr();

  for (int i4 = 0; i4 < 20; i4++) {
    EXPECT_EQ(y[i4 * 20 * 20 * 20], 100 * 100 * 100 * i4);
    ;
  }
}

TEST(checkPut, storage) {
  data4D x(20, 20, 20, 20);

  std::shared_ptr<storeBase> z = x.store->clone();
  int *y = (int *)x.store->getPtr();
  for (auto i = 0; i < 20 * 20 * 20 * 20; i++) y[i] = 0;
  x.store->putData(z);

  y = (int *)x.store->getPtr();

  for (int i4 = 0; i4 < 20; i4++) {
    EXPECT_EQ(y[i4 * 20 * 20 * 20], 100 * 100 * 100 * i4);
    ;
  }
}
TEST(getWindowBasic, storage) {
  data4D x(20, 20, 20, 20);
  std::shared_ptr<storeBase> z = x.store->clone();
  std::vector<int> fw(7, 0), nw(7, 1), jw(7, 1), ng(7, 1), fg(7, 0),
      blockG(7, 1);

  fw[0] = 1;
  jw[0] = 2;
  nw[0] = 3;
  ng[0] = 13;
  fg[0] = 0;
  blockG[1] = 13;
  x.store->getWindow(nw, fw, jw, x.nb,  fg, blockG, z->getPtr());
  int *y = (int *)z->getPtr();

  for (int i = 0; i < 3; i++) {
    EXPECT_EQ(y[i], 1 + 2 * i);
    ;
  }
  fw[1] = 1;
  fw[2] = 1;
  fw[3] = 1;
  fg[0] = 10;
  x.store->getWindow(nw, fw, jw, x.nb,  fg, blockG, z->getPtr());

  for (int i = 0; i < 3; i++) {
    EXPECT_EQ(y[i + 10], 1 + 2 * i + 100 + 10000 + 1000000);
    ;
  }
}

TEST(putWindowBasic, storage) {
  data4D x(20, 20, 20, 20);
  std::shared_ptr<storeBase> z = x.store->clone();
  std::vector<int> fw(7, 0), nw(7, 1), jw(7, 1), ng(8, 1), fg(7, 0),
      blockG(7, 10);

  fw[0] = 1;
  jw[0] = 2;
  nw[0] = 3;
  ng[0] = 10;
  fg[0] = 3;
  x.store->putWindow(nw, fw, jw, x.nb,  fg, blockG, z->getPtr());
  int *y = (int *)x.store->getPtr();

  for (int i = 0; i < 3; i++) {
    EXPECT_EQ(y[1 + 2 * i], i + 3);
  }
}
