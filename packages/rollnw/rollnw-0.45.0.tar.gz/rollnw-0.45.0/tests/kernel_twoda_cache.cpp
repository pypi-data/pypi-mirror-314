#include <gtest/gtest.h>

#include <nw/kernel/Kernel.hpp>
#include <nw/kernel/TwoDACache.hpp>

using namespace std::literals;
namespace nwk = nw::kernel;

TEST(Kernel2daCache, Get)
{
    auto mod = nwk::load_module("test_data/user/modules/DockerDemo.mod");
    EXPECT_TRUE(mod);

    auto s1 = nwk::twodas().get("placeables");
    EXPECT_TRUE(s1);
    auto s2 = nwk::twodas().get("placeables");
    EXPECT_EQ(s1, s2);
    auto s3 = nwk::twodas().get("dontexist");
    EXPECT_FALSE(s3);
    auto s4 = nwk::twodas().get(nw::Resource{"test"sv, nw::ResourceType::png});
    EXPECT_FALSE(s4);
}
