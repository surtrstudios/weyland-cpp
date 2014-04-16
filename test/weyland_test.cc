#include "gtest/gtest.h"

TEST(AssertTest, AlwaysFail) {
    EXPECT_EQ(2, 2);
}