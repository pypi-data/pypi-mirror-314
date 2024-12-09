#include <gtest/gtest.h>

#include "nw/kernel/Memory.hpp"
#include "nw/kernel/Resources.hpp"
#include "nw/resources/Erf.hpp"
#include "nw/resources/NWSync.hpp"
#include "nw/resources/Zip.hpp"

using namespace std::literals;
namespace nwk = nw::kernel;

TEST(KernelResources, AddContainer)
{
    auto rm = new nw::kernel::Resources{nwk::global_allocator()};
    auto sz = rm->size();
    nw::Erf e("test_data/user/modules/DockerDemo.mod");
    EXPECT_TRUE(rm->add_custom_container(&e, false));
    EXPECT_TRUE(rm->contains({"module"sv, nw::ResourceType::ifo}));
    EXPECT_EQ(rm->size(), sz + e.size());

    nw::kernel::Resources rm2{nwk::global_allocator(), rm};
    EXPECT_TRUE(rm2.contains({"module"sv, nw::ResourceType::ifo}));

    delete rm;
}

TEST(KernelResources, Extract)
{
    auto rm = new nw::kernel::Resources{nwk::global_allocator()};
    EXPECT_TRUE(rm->add_custom_container(new nw::Erf("test_data/user/modules/DockerDemo.mod")));
    EXPECT_TRUE(rm->add_custom_container(new nw::Zip("test_data/user/modules/module_as_zip.zip")));
    EXPECT_FALSE(rm->add_custom_container(new nw::Zip("test_data/user/modules/module_as_zip.zip")));
    EXPECT_TRUE(rm->contains({"module"sv, nw::ResourceType::ifo}));
    EXPECT_TRUE(rm->contains({"test_area"sv, nw::ResourceType::are}));
    EXPECT_EQ(rm->extract(std::regex(".*"), "tmp"), 37);
    rm->clear_containers();
    EXPECT_FALSE(rm->contains({"test_area"sv, nw::ResourceType::are}));

    delete rm;
}

TEST(KernelResources, LoadModule)
{
    auto rm = new nw::kernel::Resources{nwk::global_allocator()};
    auto path = nw::kernel::config().user_path() / "nwsync";
    auto n = nw::NWSync(path);
    EXPECT_TRUE(n.is_loaded());
    auto manifests = n.manifests();

    if (manifests.size() > 0) {
        EXPECT_TRUE(rm->load_module("test_data/user/modules/DockerDemo.mod", manifests[0]));

    } else {
        EXPECT_TRUE(rm->load_module("test_data/user/modules/DockerDemo.mod"));
    }
    delete rm;
}

TEST(KernelResources, LoadPlayerCharacter)
{
    auto mod = nwk::load_module("test_data/user/modules/DockerDemo.mod");
    EXPECT_TRUE(mod);

    auto data = nwk::resman().demand_server_vault("CDKEY", "testsorcpc1");
    EXPECT_TRUE(data.bytes.size());

    data = nwk::resman().demand_server_vault("WRONGKEY", "testsorcpc1");
    EXPECT_FALSE(data.bytes.size());

    data = nwk::resman().demand_server_vault("CDKEY", "WRONGNAME");
    EXPECT_FALSE(data.bytes.size());
}

TEST(KernelResources, Teture)
{
    auto mod = nwk::load_module("test_data/user/modules/DockerDemo.mod");
    EXPECT_TRUE(mod);

    auto tex1 = nwk::resman().texture("doesn'texist"sv);
    EXPECT_FALSE(tex1);

    auto tex2 = nwk::resman().texture("tno01_wtcliff01"sv);
    EXPECT_TRUE(tex2);
    EXPECT_TRUE(tex2->valid());
}

TEST(KernelResources, visit)
{
    auto rm = new nw::kernel::Resources{nwk::global_allocator()};
    auto sz = rm->size();
    nw::Erf e("test_data/user/modules/DockerDemo.mod");
    EXPECT_TRUE(rm->add_custom_container(&e, false));
    EXPECT_TRUE(rm->contains({"module"sv, nw::ResourceType::ifo}));

    size_t count = 0;
    auto visitor = [&count](const nw::Resource&) {
        ++count;
    };

    rm->visit(visitor);
    EXPECT_EQ(rm->size(), sz + e.size());
    delete rm;
}
