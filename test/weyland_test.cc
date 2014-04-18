#include "gtest/gtest.h"
#include "weyland/version.h"
#include "weyland/package.h"

TEST(WeylandTests, HasCorrectVersion) {
    EXPECT_EQ("0.1.0", weyland::Version);
}

TEST(PackageTests, CtroInitializesValues) {
	weyland::Package pkg;
	weyland::Package pkg2("test");
	weyland::Package pkg3("test", "0.1.0");

	EXPECT_EQ("",    pkg.name());
	EXPECT_EQ("dev", pkg.version());

	EXPECT_EQ("test", pkg2.name());
	EXPECT_EQ("dev",  pkg2.version());

	EXPECT_EQ("test",  pkg3.name());
	EXPECT_EQ("0.1.0", pkg3.version());
}
