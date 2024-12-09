#include "Tokenizer.hpp"

#include <stdexcept>

namespace nw {

Tokenizer::Tokenizer()
    : comment_{""}
{
}

Tokenizer::Tokenizer(StringView buffer, StringView comment, bool skip_newline)
    : buffer_{buffer}
    , comment_{comment}
    , skip_newline_{skip_newline}
{
}

StringView Tokenizer::current() const
{
    return current_;
}

bool Tokenizer::is_newline(StringView tk) const
{
    return tk.size() > 0 && (tk[0] == '\r' || tk[0] == '\n');
}

size_t Tokenizer::line() const
{
    return line_count_;
}

StringView Tokenizer::next()
{
    if (stack_.size()) {
        auto temp = current_ = stack_.top();
        stack_.pop();
        return temp;
    }

    StringView result;
    while (pos_ < buffer_.size()) {
        switch (buffer_[pos_]) {
        default:
            if (!comment_.empty() && pos_ + comment_.size() < buffer_.size()) {
                auto comment = StringView(&buffer_[pos_], comment_.size());
                if (comment_ == comment) {
                    pos_ += comment_.size();
                    while (pos_ < buffer_.size()) {
                        if (buffer_[pos_] == '\r' || buffer_[pos_] == '\n') break;
                        ++pos_;
                    }
                    continue;
                }
            }

            start_ = pos_++;
            while (pos_ < buffer_.size()) {
                if (buffer_[pos_] == ' '
                    || buffer_[pos_] == '\t'
                    || buffer_[pos_] == '\r'
                    || buffer_[pos_] == '\n') {
                    end_ = pos_;
                    break;
                }
                ++pos_;
            }
            if (pos_ == buffer_.size()) end_ = buffer_.size();
            result = StringView(&buffer_[start_], end_ - start_);

            break;
        case '"':
            start_ = ++pos_;
            while (pos_ < buffer_.size()) {
                if (buffer_[pos_] == '"' && buffer_[pos_ - 1] != '\\') {
                    end_ = pos_;
                    break;
                }
                ++pos_;
            }
            if (pos_ == buffer_.size() || buffer_[pos_] != '"')
                throw std::runtime_error("Unterminated quote.");
            ++pos_;

            result = StringView(&buffer_[start_], end_ - start_);
            break;
        case '\r':
        case '\n':
            start_ = pos_;
            if (buffer_[pos_] == '\r') ++pos_;
            if (pos_ < buffer_.size() && buffer_[pos_] == '\n') ++pos_;
            if (!skip_newline_) {
                result = StringView(&buffer_[start_], pos_ - start_);
            }
            ++line_count_;
            break;
        case ' ':
        case '\t':
            ++pos_;
            break;
        }
        if (result.size())
            break;
    }
    return current_ = result;
}

void Tokenizer::put_back(StringView token)
{
    current_ = token;
    stack_.push(token);
}

void Tokenizer::set_buffer(StringView buffer)
{
    buffer_ = buffer;
}

inline bool is_newline(StringView tk)
{
    if (tk.empty()) return false;
    return tk[0] == '\r' || tk[0] == '\n';
}

} // namespace nw
