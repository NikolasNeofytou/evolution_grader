#include <gtest/gtest.h>
#include <rapidcheck.h>

int sum(int, int);

TEST(Sum, CommutativeProperty) {
    rc::check("commutative", [](int a, int b) {
        RC_ASSERT(sum(a, b) == sum(b, a));
    });
}

TEST(Sum, IdentityZeroProperty) {
    rc::check("identity_zero", [](int a) {
        RC_ASSERT(sum(a, 0) == a);
    });
}
