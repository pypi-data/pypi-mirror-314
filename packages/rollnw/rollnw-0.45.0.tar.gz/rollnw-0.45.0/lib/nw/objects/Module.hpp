#pragma once

#include "../i18n/LocString.hpp"
#include "../serialization/Serialization.hpp"
#include "../util/ByteArray.hpp"
#include "../util/Variant.hpp"
#include "LocalData.hpp"
#include "ObjectBase.hpp"

#include <glm/glm.hpp>
#include <stduuid/uuid.h>

namespace nw {

struct Area;

// For our purpose..  Module is going to be synonym to module.ifo.  NOT the Erf Container.

struct ModuleScripts {
    ModuleScripts() = default;

    bool from_json(const nlohmann::json& archive);
    nlohmann::json to_json() const;

    Resref on_client_enter;
    Resref on_client_leave;
    Resref on_cutsnabort;
    Resref on_heartbeat;
    Resref on_item_acquire;
    Resref on_item_activate;
    Resref on_item_unaquire;
    Resref on_load;
    Resref on_player_chat;
    Resref on_player_death;
    Resref on_player_dying;
    Resref on_player_equip;
    Resref on_player_level_up;
    Resref on_player_rest;
    Resref on_player_uneqiup;
    Resref on_spawnbtndn;
    Resref on_start;
    Resref on_user_defined;
};

struct Module : public ObjectBase {
    Module();
    Module(nw::MemoryResource* allocator);

    using AreaVariant = Variant<Vector<Resref>, Vector<Area*>>;

    static constexpr int json_archive_version = 1;
    static constexpr ObjectType object_type = ObjectType::module;
    static constexpr ResourceType::type restype = ResourceType::ifo;
    static constexpr StringView serial_id{"IFO"};

    // LCOV_EXCL_START
    virtual Module* as_module() override { return this; }
    virtual const Module* as_module() const override { return this; }
    // LCOV_EXCL_STOP

    virtual void clear() override;
    virtual bool instantiate() override;

    size_t area_count() const noexcept;
    Area* get_area(size_t index);
    const Area* get_area(size_t index) const;

    // Serialization
    static bool deserialize(Module* ent, const nlohmann::json& archive);
    static bool serialize(const Module* ent, nlohmann::json& archive);

    LocalData locals;
    ModuleScripts scripts;
    AreaVariant areas;
    LocString description;
    Resref entry_area;
    glm::vec3 entry_orientation;
    glm::vec3 entry_position;
    Vector<String> haks;
    ByteArray id;
    String min_game_version;
    LocString name;
    Resref start_movie;
    String tag;
    String tlk;
    uuids::uuid uuid;

    int32_t creator = 0;
    uint32_t start_year;
    uint32_t version = 3;

    uint16_t expansion_pack = 0;

    uint8_t dawn_hour = 0;
    uint8_t dusk_hour = 0;
    bool is_save_game = false;
    uint8_t minutes_per_hour = 0;
    uint8_t start_day = 0;
    uint8_t start_hour = 0;
    uint8_t start_month = 0;
    uint8_t xpscale = 0;

    bool instantiated_ = false;
};

// == Module - Serialization - Gff ============================================
// ============================================================================

bool deserialize(Module* ent, const GffStruct& archive);
GffBuilder serialize(const Module* ent);
bool serialize(const Module* ent, GffBuilderStruct& archive);

bool deserialize(ModuleScripts& self, const GffStruct& archive);
bool serialize(const ModuleScripts& self, GffBuilderStruct& archive);

} // namespace nw
