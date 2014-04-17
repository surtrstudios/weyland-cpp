#include "gtest/gtest.h"
#include "weyland/version.h"

TEST(WeylandTests, HasCorrectVersion) {
    EXPECT_EQ("0.1.0", weyland::Version);
}