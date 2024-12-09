#pragma once

#include "../objects/ObjectHandle.hpp"
#include "../util/FixedVector.hpp"
#include "Spell.hpp"
#include "Versus.hpp"
#include "rule_type.hpp"

namespace nw {

// == Effect ==================================================================
// ============================================================================

DECLARE_RULE_TYPE(EffectType);

struct EffectHandle;

enum struct EffectCategory {
    magical,
    extraordinary,
    supernatural,
    item,
    innate,
};

struct EffectID {
    uint32_t version = 0;
    uint32_t index = 0;
};

struct Effect {
    Effect(nw::MemoryResource* allocator = nw::kernel::global_allocator());
    Effect(EffectType type_, nw::MemoryResource* allocator = nw::kernel::global_allocator());

    /// Clears the effect such that it's as if default constructed
    void clear();

    /// Gets a floating point value
    float get_float(size_t index) const noexcept;

    /// Gets an integer point value
    int get_int(size_t index) const noexcept;

    /// Gets a string value
    StringView get_string(size_t index) const noexcept;

    /// Gets the effect's handle
    EffectHandle handle() noexcept;

    /// Gets the effect's ID
    EffectID id() const noexcept;

    /// Sets a floating point value
    void set_float(size_t index, float value);

    /// Sets effect's ID
    void set_id(EffectID id);

    /// Sets an integer point value
    void set_int(size_t index, int value);

    /// Sets a string value
    void set_string(size_t index, String value);

    /// Sets the versus value
    void set_versus(Versus vs);

    /// Gets the versus value
    const Versus& versus() const noexcept;

    EffectType type = EffectType::invalid();
    EffectCategory category = EffectCategory::magical;
    int subtype = -1;
    ObjectHandle creator;
    Spell spell_id = Spell::invalid();
    float duration = 0.0f;
    uint32_t expire_day = 0;
    uint32_t expire_time = 0;

private:
    EffectID id_;

    FixedVector<int> integers_;
    FixedVector<float> floats_;
    FixedVector<String> strings_;
    Versus versus_;
};

struct EffectHandle {
    EffectType type = EffectType::invalid();
    int subtype = -1;
    ObjectHandle creator;
    Spell spell_id = Spell::invalid();
    EffectCategory category = EffectCategory::magical;
    Effect* effect = nullptr;

    bool operator==(const EffectHandle&) const = default;
    auto operator<=>(const EffectHandle&) const = default;
};

} // namespace nw
