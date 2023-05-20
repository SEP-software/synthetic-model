#include <gtest/gtest.h>  // googletest header file
#include <iostream>
#include <string>

#include "synModel.h"

#include "ioModes.h"

using std::string;
using namespace SEP;
using namespace sepSynthetic;

std::shared_ptr<model> createSimpleModel() {
  std::vector<axis> as;
  as.push_back(axis(20, 0., 1.));
  as.push_back(axis(20, 0., 1.));
  as.push_back(axis(20, 0., 1.));
  std::vector<std::string> props;
  props.push_back("velocity");
  ioModes io = ioModes(props);  // Dummy initialization

  std::shared_ptr<model> mod(new model(io.getDefaultIO(), as, props, 5.));
  return mod;
}
void checkBasic(std::shared_ptr<model> myMod) {
  std::shared_ptr<array3DF> vel = myMod->getProp("velocity");
  std::shared_ptr<array3DI> lay = myMod->getLayer();

  EXPECT_EQ(vel->getHyper()->getN123(), 8000);
  float *v = vel->getVals();
  int *l = lay->getVals();
  for (auto i = 0; i < 8000; i++) {
    EXPECT_EQ(v[i], 5.);
    EXPECT_EQ(l[i], 0);
  }
}
TEST(createModel, basicCLone) {
  std::shared_ptr<model> myMod = createSimpleModel();
  checkBasic(myMod);
  std::shared_ptr<model> myClone = myMod->clone();
  checkBasic(myClone);
}

TEST(model, expand) {
  std::shared_ptr<model> myMod = createSimpleModel();
  EXPECT_EQ(5., myMod->getBasement());
  myMod->expandModel(4, 3);

  std::shared_ptr<array3DF> vel = myMod->getProp("velocity");
  std::shared_ptr<array3DI> lay = myMod->getLayer();

  EXPECT_EQ(vel->getHyper()->getN123(), 20 * 20 * 27);
  float *v = vel->getVals();
  int *l = lay->getVals();
  for (auto j = 0; j < 400; j++) {
    for (auto i = 0; i < 4; i++) EXPECT_EQ(l[i + j * 27], -1);
    for (auto i = 0; i < 20; i++) EXPECT_EQ(l[i + 4 + j * 27], 0);
    for (auto i = 0; i < 3; i++) EXPECT_EQ(l[i + 24 + j * 27], -1);
  }
}

TEST(model, findZero) {
  std::shared_ptr<model> myMod = createSimpleModel();

  array2DI l1 = myMod->findNoLayer();
  myMod->expandModel(0, 3);

  array2DI l2 = myMod->findNoLayer();
  myMod->expandModel(4, 3);

  array2DI l3 = myMod->findNoLayer();

  int *a1 = l1.getVals(), *a2 = l2.getVals(), *a3 = l3.getVals();

  for (auto i = 0; i < 400; i++) {
    EXPECT_EQ(a1[i], -1);
    EXPECT_EQ(a2[i], -1);
    EXPECT_EQ(a3[i], 3);
  }
}
