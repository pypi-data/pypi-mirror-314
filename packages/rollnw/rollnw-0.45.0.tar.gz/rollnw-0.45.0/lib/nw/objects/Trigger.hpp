#pragma once

#include "../serialization/Serialization.hpp"
#include "Common.hpp"
#include "ObjectBase.hpp"
#include "Trap.hpp"

#include <glm/glm.hpp>

namespace nw {

struct TriggerScripts {
    bool from_json(const nlohmann::json& archive);
    nlohmann::json to_json() const;

    Resref on_click;
    Resref on_disarm;
    Resref on_enter;
    Resref on_exit;
    Resref on_heartbeat;
    Resref on_trap_triggered;
    Resref on_user_defined;
};

struct Trigger : public ObjectBase {
    static constexpr int json_archive_version = 1;
    static constexpr ObjectType object_type = ObjectType::trigger;
    static constexpr ResourceType::type restype = ResourceType::utt;
    static constexpr StringView serial_id{"UTT"};

    Trigger();
    Trigger(nw::MemoryResource* allocator);

    // LCOV_EXCL_START
    virtual Common* as_common() override { return &common; }
    virtual const Common* as_common() const override { return &common; }
    virtual Trigger* as_trigger() override { return this; }
    virtual const Trigger* as_trigger() const override { return this; }
    // LCOV_EXCL_STOP

    virtual bool instantiate() override { return true; }
    virtual InternedString tag() const override { return common.tag; }
    virtual Versus versus_me() const override;

    // Serialization
    static bool deserialize(Trigger* obj, const nlohmann::json& archive, SerializationProfile profile);
    static bool serialize(const Trigger* obj, nlohmann::json& archive, SerializationProfile profile);
    static String get_name_from_file(const std::filesystem::path& path);

    Common common;
    Trap trap;
    TriggerScripts scripts;
    Vector<glm::vec3> geometry;
    String linked_to;

    uint32_t faction = 0;
    float highlight_height = 0.0f;
    int32_t type = 0;

    uint16_t loadscreen = 0;
    uint16_t portrait = 0;

    uint8_t cursor = 0;
    uint8_t linked_to_flags = 0;

    bool instantiated_ = false;
};

// == Trigger - Serialization - Gff ===========================================
// ============================================================================

bool deserialize(Trigger* obj, const GffStruct& archive, SerializationProfile profile);
GffBuilder serialize(const Trigger* obj, SerializationProfile profile);
bool serialize(const Trigger* obj, GffBuilderStruct& archive, SerializationProfile profile);

} // namespace nw
