#include "Common.hpp"

#include "../kernel/Strings.hpp"
#include "../serialization/Gff.hpp"

#include <nlohmann/json.hpp>

namespace nw {

Common::Common()
    : Common(nw::kernel::global_allocator())
{
}

Common::Common(nw::MemoryResource*)
{
}

void Common::clear()
{
    uuid = uuids::uuid{};
    resref = Resref{};
    tag = InternedString{};
    name = LocString{};
    locals.clear_all();
    location = Location{};

    comment.clear();
    palette_id = std::numeric_limits<uint8_t>::max();
}

bool Common::from_json(const nlohmann::json& archive, SerializationProfile profile, ObjectType object_type)
{
    String temp;
    archive.at("object_type").get_to(object_type);
    archive.at("resref").get_to(resref);
    archive.at("tag").get_to(temp);
    if (!temp.empty()) { tag = nw::kernel::strings().intern(temp); }

    if (object_type != ObjectType::creature) {
        archive.at("name").get_to(name);
    }

    locals.from_json(archive.at("locals"));

    if (profile == SerializationProfile::instance || profile == SerializationProfile::savegame) {
        archive.at("location").get_to(location);
    }

    if (profile == SerializationProfile::blueprint) {
        archive.at("comment").get_to(comment);
        archive.at("palette_id").get_to(palette_id);
    }

    return true;
}

nlohmann::json Common::to_json(SerializationProfile profile, ObjectType object_type) const
{
    nlohmann::json j;

    j["object_type"] = object_type;
    j["resref"] = resref;
    j["tag"] = tag ? tag.view() : "";

    if (object_type != ObjectType::creature) {
        j["name"] = name;
    }

    j["locals"] = locals.to_json(profile);

    if (profile == SerializationProfile::instance || profile == SerializationProfile::savegame) {
        j["location"] = location;
    }

    if (profile == SerializationProfile::blueprint) {
        j["comment"] = comment;
        j["palette_id"] = palette_id;
    }

    return j;
}

bool deserialize(Common& self, const GffStruct& archive, SerializationProfile profile, ObjectType object_type)
{
    deserialize(self.location, archive, profile);
    deserialize(self.locals, archive);

    if (!archive.get_to("TemplateResRef", self.resref, false)
        && !archive.get_to("ResRef", self.resref, false)) { // Store blueprints do their own thing
        LOG_F(ERROR, "invalid object no resref");
        return false;
    }

    if (object_type != ObjectType::creature
        && object_type != ObjectType::area
        && !archive.get_to("LocalizedName", self.name, false)
        && !archive.get_to("LocName", self.name, false)) {
        LOG_F(WARNING, "object no localized name");
    }

    String temp;
    archive.get_to("Tag", temp);
    if (!temp.empty()) { self.tag = nw::kernel::strings().intern(temp); }

    if (profile == SerializationProfile::blueprint) {
        archive.get_to("Comment", self.comment);
        archive.get_to("PaletteID", self.palette_id);
    }

    return true;
}

} // namespace nw
