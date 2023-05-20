#include <gtest/gtest.h>  // googletest header file
#include <iostream>
#include <string>

#include "deposit.h"
#include "synModel.h"

#include "dictParams.h"
#include "ioModes.h"

using std::string;
using namespace SEP;
using namespace sepSynthetic;

std::shared_ptr<model> createSimpleModel(std::shared_ptr<genericIO> gio,
                                         std::vector<std::string> props) {
  std::vector<axis> as;
  as.push_back(axis(20, 0., 1.));
  as.push_back(axis(20, 0., 1.));
  as.push_back(axis(20, 0., 1.));

  std::shared_ptr<model> mod(new model(gio, as, props, 5.));
  return mod;
}

TEST(deposit, simple) {
  std::map<std::string, std::string> pars;
  std::vector<std::string> props;
  props.push_back("velocity");
  ioModes io = ioModes(props);  // Dummy initialization

  std::shared_ptr<dictParams> dpars(new dictParams(pars));
  std::shared_ptr<genericIO> gpars = io.getDefaultIO();
  gpars->replaceParamObj(dpars);

  std::shared_ptr<model> myMod = createSimpleModel(gpars, props);

  pars["dev_layer"] = "0.";
  pars["var"] = "0.";
  pars["layer_rand"] = "0.";
  pars["thick"] = "10";
  pars["prop"] = "4.";
  dpars->resetParams(pars);

  std::shared_ptr<deposit> dep(new deposit(gpars, props));
  dep->updateParams();
  dep->doAction(*(myMod.get()));

  std::shared_ptr<array3DF> vel = myMod->getProp("velocity");
  std::shared_ptr<array3DI> lay = myMod->getLayer();

  EXPECT_EQ(vel->getHyper()->getN123(), 20 * 20 * 30);
  float *v = vel->getVals();
  int *l = lay->getVals();
  for (auto j = 0; j < 400; j++) {
    for (auto i = 0; i < 10; i++) EXPECT_EQ(l[i + j * 30], 1);
    for (auto i = 0; i < 20; i++) EXPECT_EQ(l[i + 10 + j * 30], 0);
    for (auto i = 0; i < 10; i++) EXPECT_EQ(v[i + j * 30], 4.);
    for (auto i = 0; i < 20; i++) EXPECT_EQ(v[i + 10 + j * 30], 5.);
  }
}
TEST(deposit, layered) {
  std::map<std::string, std::string> pars;
  std::vector<std::string> props;
  props.push_back("velocity");
  ioModes io = ioModes(props);  // Dummy initialization

  std::shared_ptr<dictParams> dpars(new dictParams(pars));
  std::shared_ptr<genericIO> gpars = io.getDefaultIO();
  gpars->replaceParamObj(dpars);

  std::shared_ptr<model> myMod = createSimpleModel(gpars, props);

  pars["dev_layer"] = "0.1";
  pars["var"] = "0.";
  pars["thick"] = "10";
  pars["prop"] = "4.";
  dpars->resetParams(pars);

  std::shared_ptr<deposit> dep(new deposit(gpars, props));
  dep->updateParams();
  dep->doAction(*(myMod.get()));

  std::shared_ptr<array3DF> vel = myMod->getProp("velocity");
  std::shared_ptr<array3DI> lay = myMod->getLayer();

  EXPECT_EQ(vel->getHyper()->getN123(), 20 * 20 * 30);
  float *v = vel->getVals();
  int *l = lay->getVals();
  for (auto j = 0; j < 400; j++) {
    for (auto i = 0; i < 10; i++) EXPECT_EQ(l[i + j * 30], 1);
    for (auto i = 0; i < 20; i++) EXPECT_EQ(l[i + 10 + j * 30], 0);
    for (auto i = 0; i < 10; i++) EXPECT_LE(v[i + j * 30], 4.1);
    for (auto i = 0; i < 10; i++) EXPECT_GE(v[i + j * 30], 3.9);

    for (auto i = 0; i < 20; i++) EXPECT_EQ(v[i + 10 + j * 30], 5.);
  }
}
TEST(deposit, vz) {
  std::map<std::string, std::string> pars;
  std::vector<std::string> props;
  props.push_back("velocity");
  ioModes io = ioModes(props);  // Dummy initialization

  std::shared_ptr<dictParams> dpars(new dictParams(pars));
  std::shared_ptr<genericIO> gpars = io.getDefaultIO();
  gpars->replaceParamObj(dpars);

  std::shared_ptr<model> myMod = createSimpleModel(gpars, props);

  pars["dev_layer"] = "0.";
  pars["var"] = "0.1";
  pars["layer_rand"] = "0.";
  pars["thick"] = "10";
  pars["prop"] = "4.";
  dpars->resetParams(pars);

  std::shared_ptr<deposit> dep(new deposit(gpars, props));
  dep->updateParams();
  dep->doAction(*(myMod.get()));

  std::shared_ptr<array3DF> vel = myMod->getProp("velocity");
  std::shared_ptr<array3DI> lay = myMod->getLayer();

  EXPECT_EQ(vel->getHyper()->getN123(), 20 * 20 * 30);
  float *v = vel->getVals();
  int *l = lay->getVals();
  for (auto j = 0; j < 400; j++) {
    for (auto i = 0; i < 10; i++) EXPECT_EQ(l[i + j * 30], 1);
    for (auto i = 0; i < 20; i++) EXPECT_EQ(l[i + 10 + j * 30], 0);
    for (auto i = 0; i < 10; i++) EXPECT_LE(v[i + j * 30], 4.41);
    for (auto i = 0; i < 10; i++) EXPECT_GE(v[i + j * 30], 3.59);
  }
}
