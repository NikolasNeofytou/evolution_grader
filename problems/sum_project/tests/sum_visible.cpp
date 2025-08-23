#include <gtest/gtest.h>

int sum(int, int);

TEST(Sum, Small) {
    EXPECT_EQ(sum(2, 3), 5);
}

TEST(Sum, Negatives) {
    EXPECT_EQ(sum(-4, 1), -3);
}

TEST(Sum, Zero) {
    EXPECT_EQ(sum(0, 0), 0);
}
