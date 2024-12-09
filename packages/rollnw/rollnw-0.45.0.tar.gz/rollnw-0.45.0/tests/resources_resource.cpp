#include <gtest/gtest.h>

#include <nw/log.hpp>
#include <nw/resources/Resource.hpp>

using namespace nw;
using namespace std::literals;

TEST(Resource, FromPath)
{
    std::filesystem::path p1{"test.utc"};
    auto r1 = Resource::from_path(p1);
    EXPECT_TRUE(r1.valid());

    std::filesystem::path p2{"test.xxx"};
    auto r2 = Resource::from_path(p2);
    EXPECT_FALSE(r2.valid());

    std::filesystem::path p3{".xxx"};
    auto r3 = Resource::from_path(p3);
    EXPECT_FALSE(r3.valid());

    std::filesystem::path p4{""};
    auto r4 = Resource::from_path(p4);
    EXPECT_FALSE(r4.valid());

    std::filesystem::path p5{"test/test.ini"};
    auto r5 = Resource::from_path(p5);
    EXPECT_TRUE(r5.valid());

    std::filesystem::path p6{"test/test_this_is_too_long_for_resref_of_32_chars.ini"};
    auto r6 = Resource::from_path(p6);
    EXPECT_FALSE(r6.valid());
}

TEST(Resource, FromFilename)
{
    std::string p1{"test.utc"};
    auto r1 = Resource::from_filename(p1);
    EXPECT_TRUE(r1.valid());

    std::string p2{"test.xxx"};
    auto r2 = Resource::from_filename(p2);
    EXPECT_FALSE(r2.valid());

    std::string p3{".xxx"};
    auto r3 = Resource::from_filename(p3);
    EXPECT_FALSE(r3.valid());

    std::string p4{""};
    auto r4 = Resource::from_filename(p4);
    EXPECT_FALSE(r4.valid());

    std::string p6{"test_this_is_too_long_for_resref_of_32_chars.ini"};
    auto r6 = Resource::from_filename(p6);
    EXPECT_FALSE(r6.valid());
}

TEST(Resource, Resref)
{
    std::array<char, 16> test1{'t', 'e', 's', 't'};
    nw::Resref resref1(test1);
    EXPECT_EQ(resref1.view(), "test");

    std::array<char, 16> test2{'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'};
    nw::Resref resref2(test2);
    EXPECT_EQ(resref2.view(), "aaaaaaaaaaaaaaaa");

    std::array<char, 17> test3{'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'};
    nw::Resref resref3(test3);
    EXPECT_TRUE(resref3.empty());

    std::string_view test4{"aaaaaaaaaaaaaaaa"};
    nw::Resref resref4(test4);
    EXPECT_EQ(resref4.view(), "aaaaaaaaaaaaaaaa");

    std::string_view test5{"test"};
    nw::Resref resref5(test5);
    EXPECT_EQ(resref5.view(), "test");
}
