#pragma once

#include "Common.hpp"
#include "Inventory.hpp"
#include "Item.hpp"
#include "Lock.hpp"
#include "ObjectBase.hpp"
#include "Saves.hpp"
#include "Trap.hpp"

namespace nw {

DECLARE_RULE_TYPE(PlaceableType);

struct PlaceableInfo {
    PlaceableInfo(const TwoDARowView& tda);

    String label;
    uint32_t name = 0xFFFFFFFF;
    nw::Resref model;
    //  LightColor
    //  LightOffsetX
    //  LightOffsetY
    //  LightOffsetZ
    //  SoundAppType
    //  ShadowSize
    //  BodyBag
    //  LowGore
    //  Reflection
    bool static_;

    bool valid() const noexcept { return name != 0xFFFFFFFF || !label.empty(); }
};

using PlaceableArray = RuleTypeArray<PlaceableType, PlaceableInfo>;

enum struct PlaceableAnimationState : uint8_t {
    none = 0, // Technically "default"
    open = 1,
    closed = 2,
    destroyed = 3,
    activated = 4,
    deactivated = 5
};

struct PlaceableScripts {
    bool from_json(const nlohmann::json& archive);
    nlohmann::json to_json() const;

    Resref on_click;
    Resref on_closed;
    Resref on_damaged;
    Resref on_death;
    Resref on_disarm;
    Resref on_heartbeat;
    Resref on_inventory_disturbed;
    Resref on_lock;
    Resref on_melee_attacked;
    Resref on_open;
    Resref on_spell_cast_at;
    Resref on_trap_triggered;
    Resref on_unlock;
    Resref on_used;
    Resref on_user_defined;
};

struct Placeable : public ObjectBase {
    Placeable();
    Placeable(MemoryResource* allocator);
    static constexpr int json_archive_version = 1;
    static constexpr ObjectType object_type = ObjectType::placeable;
    static constexpr ResourceType::type restype = ResourceType::utp;
    static constexpr StringView serial_id{"UTP"};

    // LCOV_EXCL_START
    virtual Common* as_common() override { return &common; }
    virtual const Common* as_common() const override { return &common; }
    virtual Placeable* as_placeable() override { return this; }
    virtual const Placeable* as_placeable() const override { return this; }
    // LCOV_EXCL_STOP

    virtual void clear() override;
    virtual bool instantiate() override;
    virtual InternedString tag() const override { return common.tag; }

    // Serialization
    static bool deserialize(Placeable* obj, const nlohmann::json& archive, SerializationProfile profile);
    static bool serialize(const Placeable* obj, nlohmann::json& archive, SerializationProfile profile);
    static String get_name_from_file(const std::filesystem::path& path);

    Common common;
    PlaceableScripts scripts;
    Inventory inventory;
    Lock lock;
    Trap trap;

    Resref conversation;
    LocString description;
    Saves saves;

    uint32_t appearance = 0;
    uint32_t faction = 0;

    int16_t hp = 0;
    int16_t hp_current = 0;
    uint16_t portrait_id = 0;

    PlaceableAnimationState animation_state = PlaceableAnimationState::none;
    uint8_t bodybag = 0;
    uint8_t hardness = 0;
    bool has_inventory = false;
    bool interruptable = 0;
    bool plot = 0;
    bool static_ = false;
    bool useable = false;

    bool instantiated_ = false;
};

// == Placeable - Serialization - Gff =========================================
// ============================================================================

bool deserialize(Placeable* obj, const GffStruct& archive, SerializationProfile profile);
GffBuilder serialize(const Placeable* obj, SerializationProfile profile);
bool serialize(const Placeable* obj, GffBuilderStruct& archive, SerializationProfile profile);

bool deserialize(PlaceableScripts& self, const GffStruct& archive);
bool serialize(const PlaceableScripts& self, GffBuilderStruct& archive);

} // namespace nw
