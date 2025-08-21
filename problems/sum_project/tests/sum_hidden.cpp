#include <gtest/gtest.h>

int sum(int, int);

TEST(SumHidden, Large) {
    EXPECT_EQ(sum(1000000, 2000000), 3000000);
}

TEST(SumHidden, Mixed) {
    EXPECT_EQ(sum(-10, 10), 0);
}
