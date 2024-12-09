#pragma once

#include "../serialization/Serialization.hpp"
#include "Common.hpp"
#include "ObjectBase.hpp"

namespace nw {

struct Sound : public ObjectBase {
    static constexpr int json_archive_version = 1;
    static constexpr ObjectType object_type = ObjectType::sound;
    static constexpr ResourceType::type restype = ResourceType::uts;
    static constexpr StringView serial_id{"UTS"};

    Sound();
    Sound(nw::MemoryResource* allocator);

    // LCOV_EXCL_START
    virtual Common* as_common() override { return &common; }
    virtual const Common* as_common() const override { return &common; }
    virtual Sound* as_sound() override { return this; }
    virtual const Sound* as_sound() const override { return this; }
    // LCOV_EXCL_STOP

    virtual bool instantiate() override { return true; }
    virtual InternedString tag() const override { return common.tag; }

    static bool deserialize(Sound* obj, const nlohmann::json& archive, SerializationProfile profile);
    static void serialize(const Sound* obj, nlohmann::json& archive, SerializationProfile profile);
    static String get_name_from_file(const std::filesystem::path& path);

    Common common;
    Vector<Resref> sounds;

    float distance_min = 0.0f;
    float distance_max = 0.0f;
    float elevation = 0.0f;
    uint32_t generated_type = 0; // Instance only
    uint32_t hours = 0;
    uint32_t interval = 0;
    uint32_t interval_variation = 0;
    float pitch_variation = 0.0f;
    float random_x = 0.0f;
    float random_y = 0.0f;

    bool active = 0;
    bool continuous = 0;
    bool looping = 0;
    bool positional = 0;
    uint8_t priority = 0;
    bool random = 0;
    bool random_position = 0;
    uint8_t times = 3; // Always
    uint8_t volume = 100;
    uint8_t volume_variation = 0;

    bool instantiated_ = false;
};

// == Sound - Serialization - Gff =============================================
// ============================================================================

bool deserialize(Sound* obj, const GffStruct& archive, SerializationProfile profile);
bool serialize(const Sound* obj, GffBuilderStruct& archive, SerializationProfile profile);
GffBuilder serialize(const Sound* obj, SerializationProfile profile);

} // namespace nw
